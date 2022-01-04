// declaring varibales
let parser, lifelines, messages, fragments;
let par = [];
let val = [];
let finalConfig = [];

// extract data
export const extractData = (lifelines, messages, fragments) => {
  for (let i = 0; i < messages.length; i++) {
    if (messages[i]["$"].messageSort === "synchCall") {
      messages[i]["$"].name = messages[i]["$"].name
        .replace(/%20/g, " ")
        .replace(/%25/g, "%");
      // console.log("Parameter : "+messages[i]["$"].name);
      par.push(messages[i]["$"].name);
      if (
        messages[i]["$"].name === "Select Disabled Passenger Concession" ||
        messages[i]["$"].name === "Select Patient Concession" ||
        messages[i]["$"].name === "Select Student Concession" ||
        messages[i]["$"].name === "Select Widow Concession"
      )
        if (!messages[i + 1]["$"].name.includes("NS"))
          messages[i + 1]["$"].name = "NS or " + messages[i + 1]["$"].name;
    }

    if (messages[i]["$"].messageSort === "reply") {
      messages[i]["$"].name = messages[i]["$"].name
        .replace(/%20/g, " ")
        .replace(/%25/g, "%");
      // console.log("Value : " + messages[i]["$"].name);

      if (
        messages[i]["$"].name.includes("Sum of % of highest concession type")
      ) {
        messages[i]["$"].name = messages[i]["$"].name.split("and");
        messages[i]["$"].name = messages[i]["$"].name[1].trim();
      }
      val.push(messages[i]["$"].name);
    }
  }
};

// func to PVs
export const paramterValuesMapping = (messages, fragments) => {
  // main logic

  for (let i = 0; i < par.length; i++) {
    var my_para = par[i]; // take the first parameter

    for (let j = 0; j < messages.length; j++) {
      // check to which message name it matches
      if (my_para === messages[j]["$"].name) {
        // take send event of that message
        var send_event = messages[j]["$"].sendEvent;
        //check to which fragment xmi_id that matches
        for (let k = 0; k < fragments.length; k++) {
          if (send_event === fragments[k]["$"]["xmi:id"]) {
            // take covered of that fragment
            var covered = fragments[k]["$"].covered;
            // now search in fragments that where the same covered can be found
            for (let l = k + 1; l < fragments.length; l++) {
              if (covered === fragments[l]["$"].covered) {
                // if the covered is found. then take xmi_id of that covered
                var xmi_id = fragments[l]["$"]["xmi:id"];
                // match this xmi id to the messages recieve event
                for (let m = 0; m < messages.length; m++) {
                  if (xmi_id === messages[m]["$"].receiveEvent) {
                    // this is value of our parameter
                    var my_val = messages[m]["$"].name;
                    finalConfig.push({
                      parameter: my_para,
                      value: my_val,
                    });
                    break;
                  } else if (m === messages.length - 1) {
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
export const checkGuardCondition = (fragments) => {
  // this function checks if the guard conditions are available in the code
  var flag = 0;

  for (let i = 0; i < fragments.length; i++) {
    if (fragments[i].hasOwnProperty("operand")) {
      flag = 1;
    }
  }
  return flag;
};

// extracting guard conditions
export const extractGuardConditions = (fragments) => {
  // getting gaurd conditions
  var guard_condition_array = [];

  for (let i = 0; i < fragments.length; i++) {
    if (fragments[i].hasOwnProperty("operand")) {
      // then select that fragment
      var f = fragments[i];
      // take operand array in that fragment
      var operand_array = f["operand"];

      // traverse the operand array
      for (var j = 0; j < operand_array.length; j++) {
        // take each element one by one
        if (operand_array[j]["guard"]) {
          var condition = operand_array[j]["guard"]["$"].specification;
          // save this condition to guard condition array
          guard_condition_array.push(condition);
        }
      }

      /*
      // traverse the operand array
      for (let j = 0; j < operand_array.length; j++) {
        // take each element one by one
        var condition = operand_array[j]["guard"]["$"].specification;
        // save this condition to guard condition array
        guard_condition_array.push(condition);
      }
      */
    }
  }

  //console.log('guard conditions');
  //console.log(guard_condition_array);

  // creating json array
  var guard_condition_data = [];

  for (let i = 0; i < guard_condition_array.length; i++) {
    let condition = guard_condition_array[i];
    if (condition.includes("%3C=")) {
      let split_condition = condition.split("%3C=");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: "<=",
        value: split_condition[1],
      });
    } else if (condition.includes("%3E=")) {
      let split_condition = condition.split("%3E=");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: ">=",
        value: split_condition[1],
      });
    } else if (condition.includes("%3C")) {
      let split_condition = condition.split("%3C");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: "<",
        value: split_condition[1],
      });
    } else if (condition.includes("%3E")) {
      let split_condition = condition.split("%3E");
      guard_condition_data.push({
        parameter: split_condition[0],
        operator: ">",
        value: split_condition[1],
      });
    } else if (condition.includes("=")) {
      let split_condition = condition.split("=");
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
  let par_arr = [];
  let unique_parameters = [];

  for (let i = 0; i < guard_condition_data.length; i++) {
    par_arr.push(guard_condition_data[i].parameter);
  }

  for (let i = 0; i < par_arr.length; i++) {
    if (!unique_parameters.includes(par_arr[i])) {
      unique_parameters.push(par_arr[i]);
    }
  }

  // recent logic : putting the guard conditions parameters and values in finalConfig
  for (let i = 0; i < guard_condition_data.length; i++) {
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
    let v = finalConfig[i].value.split(" and ").join(" And ").split(" or ");
    //let q = finalConfig[i].value.split(" and ").join(" And ");
    //let v =finalConfig[i].value.split(" or ").join(" , ").split(" and ");
    //let v = finalConfig[i].value.split(" or ").join(" And ").split(" and ");
    t.push({
      p: p,
      v: v,
      //q: q,
    });
  }

  // console.log(t);

  let updated_t = [];
  let v = [];
  let selected_p = [];
  let selected_v = [];
  let flag = 0;

  for (let i = 0; i < t.length; i++) {
    flag = 0;
    selected_p.push(t[i].p);
    for (let j = i + 1; j < t.length; j++) {
      if (t[i].p === t[j].p && t[i].p in selected_p !== true) {
        // eslint-disable-next-line
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
      // eslint-disable-next-line
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

  return updated_t;
};

export const sequenceScriptRunner = (data) => {
  return new Promise((resolve, reject) => {
    data = JSON.stringify(data);
    parser = JSON.parse(data);

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

    extractData(lifelines, messages, fragments);
    paramterValuesMapping(messages, fragments);
    let flag = checkGuardCondition(fragments);
    if (flag === 1) {
      extractGuardConditions(fragments);
    }

    let result = fillPVMatrix(finalConfig);

    if (result) {
      resolve(result);
    } else {
      reject("error occurred");
    }
  });
};
