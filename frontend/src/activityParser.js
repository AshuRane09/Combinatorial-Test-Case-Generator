// func to PVs
export const paramterValuesMapping = (node_array, edges_array) => {
  let finalConfig = [];
  let edge_map = new Map();
  let multiConcession_map = new Map();
  let guard_map = new Map();
  let Infeasible_map = new Map();
  let final = new Map();

  for (let i = 0; i < edges_array.length; i++) {
    if (
      edges_array[i]["$"]["xmi:type"] === "uml:ControlFlow" &&
      edges_array[i]["$"].name
    ) {
      if (
        edges_array[i]["$"].name !== "Yes" &&
        edges_array[i]["$"].name !== "No" &&
        edges_array[i]["$"].name !== "Is%20valid"
      )
        edge_map.set(edges_array[i]["$"].target, [edges_array[i]["$"].name]);
    }

    //guard condition
    if (edges_array[i]["guard"]) {
      guard_map.set(edges_array[i]["$"].target, [
        edges_array[i]["guard"]["$"]["value"],
      ]);
    }
  }

  for (let i = 0; i < node_array.length; i++) {
    if (node_array[i]["$"]["xmi:type"] === "uml:OpaqueAction") {
      //check in edge_map
      if (edge_map.has(node_array[i]["$"]["xmi:id"])) {
        edge_map
          .get(node_array[i]["$"]["xmi:id"])
          .push(node_array[i]["$"].name);
      }

      //check in guard map
      if (guard_map.has(node_array[i]["$"]["xmi:id"])) {
        guard_map
          .get(node_array[i]["$"]["xmi:id"])
          .push(node_array[i]["$"].name);
      }
      //infeasible Concession Condition
      if (node_array[i]["$"].name === "Select%20Infeasible%20Concession") {
        i++;
        while (node_array[i]["$"].name !== "Select%20Concession%20Rules") {
          if (node_array[i]["$"]["xmi:type"] === "uml:OpaqueAction") {
            Infeasible_map.set(node_array[i]["$"]["xmi:id"], [
              node_array[i]["$"].name,
              "Infeasible%20Input",
            ]);
            if (edge_map.has(node_array[i]["$"]["xmi:id"]))
              edge_map.delete(node_array[i]["$"]["xmi:id"]);
          }
          i++;
        }
        i--;
      }

      //multi Concession Condition
      if (
        node_array[i]["$"].name === "Select%20Multiple%20Concession%20Types"
      ) {
        i++;
        while (node_array[i]["$"].name !== "Select%20Infeasible%20Concession") {
          if (node_array[i]["$"]["xmi:type"] === "uml:OpaqueAction") {
            if (edge_map.has(node_array[i]["$"]["xmi:id"])) {
              multiConcession_map.set(node_array[i]["$"]["xmi:id"], [
                edge_map.get(node_array[i]["$"]["xmi:id"])[0],
                node_array[i]["$"].name,
              ]);
              edge_map.delete(node_array[i]["$"]["xmi:id"]);
            }
          }
          i++;
        }
        i--;
      }
    }
  }

  //merge edge_map
  edge_map.forEach((value, key) => {
    value[0] = value[0].replace(/%20/g, " ");
    let parameter = value[0];
    let split_parameter;

    if (parameter.includes("Is")) {
      //add prefix-select

      split_parameter = parameter
        .split("Is ")
        .join("Select ")
        .split("?")
        .join("");

      value[0] = split_parameter;
    }

    final.set(key, value);
  });

  //MultiConcession_map
  multiConcession_map.forEach((value, key) => {
    value[0] = value[0].replace(/%20/g, " ");
    let parameter = value[0];
    let split_parameter;

    if (parameter.includes("Is")) {
      //add prefix-select and suffix-Concession
      split_parameter = parameter
        .split("Is ")
        .join("Select ")
        .split("?")
        .join(" Concession");

      value[0] = split_parameter;
    }
    final.set(key, value);
  });

  //merge Infeasible_map
  Infeasible_map.forEach((value, key) => {
    value[0] = value[0].replace(/%20/g, " ");
    final.set(key, value);
  });

  //Maximum Concession add to last
  let max_conc = guard_map.entries().next();
  if (max_conc.value[1][0] === "Maximum%20Allowed%20Concession") {
    guard_map.delete(max_conc.value[0]);
    guard_map.set(max_conc.value[0], max_conc.value[1]);
  }

  //merge guard_map
  guard_map.forEach((value, key) => {
    let condition = value[0];
    if (condition.includes("%3C=")) {
      let split_condition = condition.split("%3C=");
      value[0] = split_condition[0] + "%20<=%20" + split_condition[1];
    } else if (condition.includes("%3E=")) {
      let split_condition = condition.split("%3E=");
      value[0] = split_condition[0] + "%20>=%20" + split_condition[1];
    } else if (condition.includes("%3C")) {
      let split_condition = condition.split("%3C");
      value[0] = split_condition[0] + "%20<%20" + split_condition[1];
    } else if (condition.includes("%3E")) {
      let split_condition = condition.split("%3E");
      value[0] = split_condition[0] + "%20>%20" + split_condition[1];
    } else if (condition.includes("=")) {
      let split_condition = condition.split("=");
      value[0] = split_condition[0] + "%20=%20" + split_condition[1];
    }

    value[0] = value[0].replace(/%20/g, " ");
    if (value[0].includes("=")) {
      let split_value = value[0].split("= ");
      value[0] = split_value[1];
    } else if (value[0].includes("> ")) {
      value[0] = "If " + value[0].replace("> ", "types selected more than ");
    } else if (value[0].includes("< ")) {
      value[0] = "If " + value[0].replace("< ", "types selected less than ");
    }
    final.set(key, value);
  });

  console.log("final", final);

  //parsing final map
  final.forEach(function (value, key) {
    value[1] = value[1].replace(/%20/g, " ");
    value[1] = value[1].replace(/%25/g, "%");
    let string = value[1];

    if (string.includes("Select") || string.includes("or")) {
      let split_string = string
        .split("Select ")
        .join("")
        .split(" and ")
        .join(" And ")
        .split(" or ");
      value[1] = split_string;
    } else {
      let x = [];
      x.push(value[1]);
      value[1] = x;
    }

    finalConfig.push({
      p: value[0],
      v: value[1],
    });
  });

  return finalConfig;
};

export const activityScriptRunner = (data) => {
  return new Promise((resolve, reject) => {
    data = JSON.stringify(data);
    let parser = JSON.parse(data);

    let node_array = []; // this array will store all the decision nodes
    let edges_array = []; // this array will store all the edges
    let temp;
    temp = parser["xmi:XMI"]["uml:Model"]["packagedElement"][2]["node"];
    for (let i = 0; i < temp.length; i++) {
      node_array.push(temp[i]);
    }
    temp = parser["xmi:XMI"]["uml:Model"]["packagedElement"][2];
    console.log("temp", temp);

    temp = parser["xmi:XMI"]["uml:Model"]["packagedElement"][2]["edge"];
    for (let i = 0; i < temp.length; i++) {
      edges_array.push(temp[i]);
    }
    let result = paramterValuesMapping(node_array, edges_array);

    if (result) {
      resolve(result);
    } else {
      reject("error occurred");
    }
  });
};
