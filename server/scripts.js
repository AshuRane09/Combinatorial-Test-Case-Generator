const xml2json = require("xml-to-json");
const fs = require("fs");

// conversion of XMI to JSON
exports.convertXMITOJSON = (filepathstring) => {
  return new Promise((resolve, reject) => {
    xml2json(
      {
        input: filepathstring,
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
