import React, { useRef, useState } from "react";
import axios from "axios";
import { API } from "./backend";
import { Container, Alert } from "react-bootstrap";

function FileUpload() {
  const [values, setValues] = useState({
    error: "",
    success: "",
    dark: true,
    yellow: "",
    up_disabled: true,
    d_disabled: true,
  });
  const { error, success, dark, yellow, up_disabled, d_disabled } = values;
  const [appState, setAppState] = useState("Upload a File");
  const [file, setFile] = useState("");
  const [data, getFile] = useState({ name: "", path: "" });
  const el = useRef();
  let url = `${API}/download`;

  const handleChange = (e) => {
    const file = e.target.files[0];
    // console.log(file);
    setFile(file);
  };

  const uploadFile = () => {
    const formData = new FormData();
    formData.append("file", file);
    axios
      .post(`${API}/upload`, formData, {})
      .then((res) => {
        // console.log(res);
        getFile({
          name: res.data.name,
          path: `${API}/upload` + res.data.path,
        });
        setValues({
          ...values,
          error: "",
          success: true,
          dark: "",
          yellow: "",
          up_disabled: false,
          d_disabled: true,
        });
        setAppState("Success...!! File Uploaded");
      })
      .catch((err) => {
        setValues({
          ...values,
          error: true,
          success: "",
          dark: "",
          yellow: "",
          up_disabled: true,
          d_disabled: true,
        });
        setAppState("Error...!! File Not Uploaded");
      });
  };

  const fetchDataPso = () => {
    setAppState("*** Wait ***");
    setValues({
      ...values,
      error: "",
      success: "",
      dark: "",
      yellow: true,
      up_disabled: true,
      d_disabled: true,
    });

    axios({
      url: `${API}/pso`,
      method: "post",
    })
      .then(function (res) {
        if (res.status === 200) {
          setAppState("Success: PSO Test Case Generated with " + res.data);
          setValues({
            ...values,
            error: "",
            success: true,
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: false,
          });
        } else {
          setAppState("Error: File not Generated");
          setValues({
            ...values,
            error: true,
            success: "",
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: true,
          });
        }
      })
      .catch(function (error) {
        setAppState("Error: File not Generated");
        setValues({
          ...values,
          error: true,
          success: "",
          dark: "",
          yellow: "",
          up_disabled: false,
          d_disabled: true,
        });
      });
  };

  const fetchAllCombinations = () => {
    setAppState("*** Wait ***");
    setValues({
      ...values,
      error: "",
      success: "",
      dark: "",
      yellow: true,
      up_disabled: true,
      d_disabled: true,
    });

    axios({
      url: `${API}/brute`,
      method: "get",
    })
      .then(function (res) {
        if (res.status === 200) {
          setAppState("Success: Test Case Generated");
          setValues({
            ...values,
            error: "",
            success: true,
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: false,
          });
        } else {
          setAppState("Error: File not Generated");
          setValues({
            ...values,
            error: true,
            success: "",
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: true,
          });
        }
      })
      .catch(function (_error) {
        setAppState("Error: File not Generated");
        setValues({
          ...values,
          error: true,
          success: "",
          dark: "",
          yellow: "",
          up_disabled: false,
          d_disabled: true,
        });
      });
  };

  const fetchDataSa = () => {
    setAppState("*** Wait ***");
    setValues({
      ...values,
      error: "",
      success: "",
      dark: "",
      yellow: true,
      up_disabled: true,
      d_disabled: true,
    });

    axios({
      url: `${API}/sa`,
      method: "post",
    })
      .then(function (res) {
        if (res.status === 200) {
          setAppState("Success: SA Test Case Generated with " + res.data);
          setValues({
            ...values,
            error: "",
            success: true,
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: false,
          });
        } else {
          setAppState("Error: File not Generated");
          setValues({
            ...values,
            error: true,
            success: "",
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: true,
          });
        }
      })
      .catch(function (error) {
        setAppState("Error: File not Generated");
        setValues({
          ...values,
          error: true,
          success: "",
          dark: "",
          yellow: "",
          up_disabled: false,
          d_disabled: true,
        });
      });
  };

  const fetchDataQlpso = () => {
    setAppState("*** Wait ***");
    setValues({
      ...values,
      error: "",
      success: "",
      dark: "",
      yellow: true,
      up_disabled: true,
      d_disabled: true,
    });

    axios({
      url: `${API}/qlpso`,
      method: "get",
    })
      .then(function (res) {
        if (res.status === 200) {
          setAppState("Success: Test Case Generated");
          setValues({
            ...values,
            error: "",
            success: true,
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: false,
          });
        } else {
          setAppState("Error: File not Generated");
          setValues({
            ...values,
            error: true,
            success: "",
            dark: "",
            yellow: "",
            up_disabled: false,
            d_disabled: true,
          });
        }
      })
      .catch(function (_error) {
        setAppState("Error: File not Generated");
        setValues({
          ...values,
          error: true,
          success: "",
          dark: "",
          yellow: "",
          up_disabled: false,
          d_disabled: true,
        });
      });
  };

  const download = () => {
    setAppState("File Downloaded");
    setValues({
      ...values,
      error: "",
      success: true,
      dark: "",
      yellow: "",
      up_disabled: false,
      d_disabled: true,
    });
  };

  return (
    <div>
      <br />
      <h1>Test Case Generator</h1>
      <br />
      <div class="container">
        <div class="card border-0 shadow">
          <div class="card-body p-5">
            <div className="file-upload text-center">
              <input
                type="file"
                ref={el}
                onChange={handleChange}
                accept=".xlsx,.csv"
              />
              {"  "}
              <button onClick={uploadFile} className="upbutton btn btn-dark">
                Upload
              </button>
              <br />
              <br />
              {"  "}
              <button
                onClick={fetchAllCombinations}
                className="btn btn-primary"
                disabled={up_disabled}
              >
                Generate All Combinations
              </button>
              {"  "}
              <button
                onClick={fetchDataPso}
                className="btn btn-primary"
                disabled={up_disabled}
              >
                PSO Algorithm
              </button>
              {"  "}
              {"  "}
              <button
                onClick={fetchDataSa}
                className="btn btn-primary"
                disabled={up_disabled}
              >
                SA Algorithm
              </button>
              {"  "}
              {"  "}
              <button
                onClick={fetchDataQlpso}
                className="btn btn-primary"
                disabled={up_disabled}
              >
                QLPSO Algorithm
              </button>
              <br />
              <br />
              <a href={url}>
                {" "}
                <button
                  className="btn btn-success"
                  disabled={d_disabled}
                  onClick={download}
                >
                  Download
                </button>
              </a>
            </div>
          </div>

          <Container fluid>
            {error && (
              <Alert variant="danger">
                <h1 className="text-center">{appState}</h1>
              </Alert>
            )}
            {success && (
              <Alert variant="success">
                <h1 className="text-center">{appState}</h1>
              </Alert>
            )}
            {dark && (
              <Alert variant="dark">
                <h1 className="text-center">{appState}</h1>
              </Alert>
            )}
            {yellow && (
              <Alert variant="warning">
                <h1 className="text-center">{appState}</h1>
              </Alert>
            )}
          </Container>
        </div>
        <br />

        <div class="card border-0 shadow my-5">
          <div class="card-body p-5">
            <h4 class="text-center">Process</h4>
            <h6>1.Upload the excel file</h6>
            <h6>
              2.Click on generate test cases All Combinations/PSO/QLPSO/SA
            </h6>
            <h6>3.Once uploaded sucessfully, test cases will be generated</h6>
            <h6>4.Download the text file of generated test cases</h6>
          </div>
        </div>
      </div>
    </div>
  );
}
export default FileUpload;
