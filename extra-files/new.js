const xml2json = require("xml-to-json");
const fs = require("fs");
const readline = require("readline-sync");
const print = console.log;

// declaring varibales
let parser, lifelines, messages, fragments;
let par = new Array();
let val = new Array();
let column_number = -1;
let PVMatrix = new Array();
let finalConfig = new Array();

// conversion of XMI to JSON
const convertXMITOJSON = () => {
  return new Promise((resolve, reject) => {
    xml2json(
      {
        input: "./sequence_new.xmi",
        output: "./test.json",
      },
      function (err, result) {
        if (err) {
          console.error(err);
          reject(err);
        } else {
          resolve(result);
        }
      }
    );
  });
};

// extract data
const extractData = (lifelines, messages, fragments) => {
  for (var i = 0; i < messages.length; i++) {
    if (messages[i]["$"].messageSort === "synchCall") {
      //console.log("Parameter : "+messages[i]._name);
      messages[i]["$"].name = messages[i]["$"].name.replace(/%20/g, " ");
      par.push(messages[i]["$"].name);
    }
    if (messages[i]["$"].messageSort === "reply") {
      // console.log("Value : "+messages[i]._name);
      messages[i]["$"].name = messages[i]["$"].name.replace(/%20/g, " ");
      val.push(messages[i]["$"].name);
    }
  }
};

// func to PVs
const paramterValuesMapping = (messages, fragments) => {
  // main logic
  var k = 0;

  for (var i = 0; i < par.length; i++) {
    var my_para = par[i]; // take the first parameter

    for (var j = 0; j < messages.length; j++) {
      // check to which message name it matches
      if (my_para === messages[j]["$"].name) {
        // take send event of that message
        var send_event = messages[j]["$"].sendEvent;
        //check to which fragment xmi_id that matches
        for (var k = 0; k < fragments.length; k++) {
          if (send_event === fragments[k]["$"]["xmi:id"]) {
            // take covered of that fragment
            var covered = fragments[k]["$"].covered;
            // now search in fragments that where the same covered can be found
            for (var l = k + 1; l < fragments.length; l++) {
              if (covered === fragments[l]["$"].covered) {
                // if the covered is found. then take xmi_id of that covered
                var xmi_id = fragments[l]["$"]["xmi:id"];
                // match this xmi id to the messages recieve event
                for (var m = 0; m < messages.length; m++) {
                  if (xmi_id === messages[m]["$"].receiveEvent) {
                    // this is value of our parameter
                    var my_val = messages[m]["$"].name;
                    console.log(
                      "PARAMETER : " + my_para + " VALUE : " + my_val + "\n"
                    );
                    finalConfig.push({
                      parameter: my_para,
                      value: my_val,
                    });
                    break;
                  } else if (m == messages.length - 1) {
                    console.log(
                      "PARAMETER : " + my_para + " VALUE : NULL" + "\n"
                    );
                    finalConfig.push({
                      parameter: my_para,
                      value: my_val,
                    });
                  }
                }
                break;
              }
            }
            break;
          }
        }
      }
    }
  }
};

// check if guard conditions are available or not
const checkGuardCondition = (fragments) => {
  // this function checks if the guard conditions are available in the code
  var flag = 0;

  for (var i = 0; i < fragments.length; i++) {
    if (fragments[i].hasOwnProperty("operand")) {
      flag = 1;
      console.log("guard conditions exist.");
    }
  }
  return flag;
};

// extracting guard conditions
const extractGuardConditions = (fragments) => {
  // getting gaurd conditions
  var guard_condition_array = new Array();

  for (var i = 0; i < fragments.length; i++) {
    if (fragments[i].hasOwnProperty("operand")) {
      // then select that fragment
      var f = fragments[i];
      // take operand array in that fragment
      var operand_array = f["operand"];
      
      console.log("this is oparand array : ", operand_array);
      
      // traverse the operand array
      for (var j = 0; j < operand_array.length; j++) {
        // take each element one by one
        if(operand_array[j]["guard"]) {
        	var condition = operand_array[j]["guard"]["$"].specification;
        // save this condition to guard condition array
        guard_condition_array.push(condition);
        }
        
      }
    }
  }

  //console.log('guard conditions');
  //console.log(guard_condition_array);

  // creating json array
  var guard_condition_data = [];

  for (var i = 0; i < guard_condition_array.length; i++) {
    var condition = guard_condition_array[i];
    if (condition.includes("%3C=")) {
      var split_condition = condition.split("%3C=");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: "<=",
        value: split_condition[1],
      });
    } else if (condition.includes("%3E=")) {
      var split_condition = condition.split("%3E=");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: ">=",
        value: split_condition[1],
      });
    } else if (condition.includes("%3C")) {
      var split_condition = condition.split("%3C");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: "<",
        value: split_condition[1],
      });
    } else if (condition.includes("%3E")) {
      var split_condition = condition.split("%3E");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: ">",
        value: split_condition[1],
      });
    } else if (condition.includes("=")) {
      var split_condition = condition.split("=");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: "=",
        value: split_condition[1],
      });
    }
  }

  //console.log('json array');
  //console.log(guard_condition_data);
  //console.table(guard_condition_data);

  // now processing created json array to find matrix rows and columns

  // finding unique parameter values for columns
  var par_arr = new Array();
  var unique_parameters = new Array();

  for (var i = 0; i < guard_condition_data.length; i++) {
    par_arr.push(guard_condition_data[i].parameter);
  }

  for (var i = 0; i < par_arr.length; i++) {
    if (!unique_parameters.includes(par_arr[i])) {
      unique_parameters.push(par_arr[i]);
    }
  }

  // recent logic : putting the guard conditions parameters and values in finalConfig
  for (var i = 0; i < guard_condition_data.length; i++) {
    let p = guard_condition_data[i].parameter.replace(/%20/g, " ");
    let v = guard_condition_data[i].value.replace(/%20/g, " ");
    finalConfig.push({
      parameter: p,
      value: v,
    });
  } // guard conditions pushed in json array
};

// func to create CSV
const fillPVMatrix = (finalConfig) => {
  // create simplified json file
  let t = [];
  for (let i = 0; i < finalConfig.length; i++) {
    let p = finalConfig[i].parameter;
    let v = finalConfig[i].value.split(" or ");
    t.push({
      p: p,
      v: v,
    });
  }

  //console.log(t);

  let updated_t = [];
  let p;
  let v = [];
  let selected_p = [];
  let selected_v = [];
  let flag = 0;

  for (let i = 0; i < t.length; i++) {
    flag = 0;
    selected_p.push(t[i].p);
    for (let j = i + 1; j < t.length; j++) {
      if (t[i].p === t[j].p && t[i].p in selected_p !== true) {
        Object.values(t[j].v).map((item, index) => {
          if (item in selected_v !== true) {
            selected_v.push(item);
            v.push(item);
          }
        });
        flag = 1;
      }
    }
    if (flag !== 0) {
      Object.values(t[i].v).map((item, index) => {
        if (item in selected_v !== true) {
          selected_v.push(item);
          v.push(item);
        }
      });

      updated_t.push({
        p: t[i].p,
        v: v,
      });

      v = [];
    }
    // if flag = 0
    else {
      updated_t.push({
        p: t[i].p,
        v: Object.values(t[i].v),
      });
    }
  }

  for (let i = 0; i < updated_t.length; i++) {
    for (let j = i + 1; j < updated_t.length; j++) {
      if (t[i].p === t[j].p) {
        delete updated_t[j];
      }
    }
  }

  updated_t = updated_t.filter((item) => item);

  console.log(updated_t);

  // ------------------------------------------------------------------------------------

  // creating csv file
  flag = 0;
  for (let i = 0; i < t.length; i++) {
    // create string
    let string = "";
    let p = String(t[i].p);
    let v = t[i].v;
    string = string + p; // p added
    string = string + ",";
    for (let j = 0; j < v.length; j++) {
      if (j == v.length - 1) {
        string = string + v[j];
        break;
      }
      string = string + v[j];
      string = string + ",";
    }

    string = string + "\n";

    fs.appendFile("pv.csv", string, function (err) {
      if (err) {
        throw err;
        flag = 1;
      }
    });
  }

  if (flag != 1) console.log("csv written");
};

// main func
print("starting script..");

convertXMITOJSON()
  .then((result) => {
    result = JSON.stringify(result);

    parser = JSON.parse(result);

    //console.log();

    lifelines =
      parser["xmi:XMI"]["uml:Model"]["packagedElement"]["packagedElement"][
        "ownedMember"
      ]["lifeline"];

    messages =
      parser["xmi:XMI"]["uml:Model"]["packagedElement"]["packagedElement"][
        "ownedMember"
      ]["message"];

    fragments =
      parser["xmi:XMI"]["uml:Model"]["packagedElement"]["packagedElement"][
        "ownedMember"
      ]["fragment"];
      
     console.log(fragments);

    /*
    lifelines =
      parser["xmi:XMI"]["uml:Model"]["packagedElement"][1]["ownedMember"][
        "lifeline"
      ];

    messages =
      parser["xmi:XMI"]["uml:Model"]["packagedElement"][1]["ownedMember"][
        "message"
      ];

    fragments =
      parser["xmi:XMI"]["uml:Model"]["packagedElement"][1]["ownedMember"][
        "fragment"
      ];
      */

    // calling extract data
    extractData(lifelines, messages, fragments);

    // parameters values mapping
    paramterValuesMapping(messages, fragments);

    // checking if guard conditions are available or not!
    let flag = checkGuardCondition(fragments);
    if (flag === 1) {
      let choice = readline.question(
        "do you want to see guard conditions [y/n]: "
      );
      if (choice === "y") {
        // extract guard condition
        extractGuardConditions(fragments);
      }
      //
      else {
        console.log("invalid choice");
      }

      // calling function to create CSV
      fillPVMatrix(finalConfig);
    }
    //
    else {
      console.log("guard conditions are not available.");
    }
  })
  .catch((err) => console.log(err));

module.exports = { convertXMITOJSON };
