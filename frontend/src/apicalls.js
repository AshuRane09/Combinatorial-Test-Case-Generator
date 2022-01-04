import { API } from "./backend";
import axios from "axios";
import React from "react";
import Button from "react-bootstrap/Button";
import * as FileSaver from "file-saver";
import * as XLSX from "xlsx";

export const getJSON = (formdata) => {
  return fetch(`${API}/submit`, {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: formdata,
  })
    .then((response) => {
      return response.json();
    })
    .catch((err) => console.log("error in hitting the route!"));
};

export const ExportCSV = ({ csvData, fileName, disability }) => {
  const fileType =
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8";
  const fileExtension = ".xlsx";

  const exportToCSV = (csvData, fileName) => {
    let payload = {
      Data: csvData,
    };
    axios({
      url: `${API}/Pairs`,
      method: "post",
      data: payload,
    })
      .then(function (response) {
        const ws = XLSX.utils.json_to_sheet(response.data);
        const wb = { Sheets: { data: ws }, SheetNames: ["data"] };
        const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
        const data = new Blob([excelBuffer], { type: fileType });
        FileSaver.saveAs(data, fileName + fileExtension);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  return (
    <Button
      variant="warning"
      className="mt-2 ml-4"
      disabled={disability}
      onClick={(e) => exportToCSV(csvData, fileName)}
    >
      Export
    </Button>
  );
};
