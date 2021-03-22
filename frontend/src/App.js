import React, { useState } from "react";
import {
  Container,
  Row,
  Col,
  Form,
  Button,
  Alert,
  Table,
} from "react-bootstrap";
import { getJSON } from "./apicalls";
import { ExportCSV } from "./apicalls";
import { scriptRunner } from "./parser";
import { Link } from "react-router-dom";

const App = () => {
  const [values, setValues] = useState({
    error: "",
    success: "",
    file: "",
    pv_disabled: true,
    test_case_disabled: true,
    formData: new FormData(),
  });

  const [pv_result, setPv_result] = useState([]);

  const [infeasibleInputs, setInfeasibleInputs] = useState([]);

  const [CSV, setCSV] = useState([]);

  const [appstate, setAppstate] = useState("Upload XMI File!");

  const { error, success, formData, pv_disabled, test_case_disabled } = values;

  const handleChange = (name) => (event) => {
    let value = event.target.files[0];
    formData.set("myfile", value);
    setValues({ ...values, pv_disabled: false, [name]: value });
  };

  const onSubmitFile = (event) => {
    setAppstate("Wait...");
    event.preventDefault();
    setValues({ ...values, error: "", loading: true, success: false });
    getJSON(formData).then((data) => {
      if (data.error) {
        setValues({
          ...values,
          loading: false,
          error: data.error,
          success: false,
        });
      } else {
        scriptRunner(data).then((result) => {
          if (result) {
            setPv_result(result);
            // console.log(result);

            let temp_infeasible_arr = [];
            // storing infeasible pairs
            for (let i = 0; i < result.length; i++) {
              if (result[i].v.includes("Infeasible Input")) {
                // saperate by coma
                let temp = result[i].p.split(",");
                temp_infeasible_arr.push({
                  p1: temp[0],
                  p2: temp[1],
                });
              }
            }

            setInfeasibleInputs(temp_infeasible_arr);

            const x = [];
            for (let i = 0; i < result.length; i++) {
              //console.log(result[i].p);
              //console.log(result[i].v.join(","));
              x.push({
                parameter: result[i].p,
                values: result[i].v.join(","),
              });
            }
            setCSV(x);
            setAppstate("Generated Successfully!!");
          }
        });
        setValues({
          ...values,
          error: "",
          success: true,
          test_case_disabled: false,
          formData: "",
        });
      }
    });
  };

  const pvPrinter = () => {
    //console.log("this is pv_result", pv_result);
    if (pv_result.length !== 0) {
      return (
        <div>
          <Table striped bordered hover variant="dark">
            <thead>
              <tr>
                <th>Sr. No</th>
                <th>Parameters</th>
                <th>Values</th>
              </tr>
            </thead>
            <tbody>
              {pv_result.map((item, index) => {
                // eslint-disable-next-line
                if (!item.v.includes("Infeasible Input")) {
                  return (
                    <tr key={index}>
                      <td>{index}</td>
                      <td>{item.p}</td>
                      {item.v.map((value, index) => {
                        return <td key={index}>{value + " "}</td>;
                      })}
                    </tr>
                  );
                }
              })}
            </tbody>
          </Table>

          {infeasibleInputs.length === 0 ? (
            <div>
              <p className="text-center">No infeasible inputs present.</p>
            </div>
          ) : (
            <div>
              <p className="text-center">Infeasible Inputs</p>

              <Table striped bordered hover variant="dark">
                <thead>
                  <tr>
                    <th>Sr. No</th>
                    <th>1</th>
                    <th>2</th>
                  </tr>
                </thead>
                <tbody>
                  {infeasibleInputs.map((item, index) => {
                    return (
                      <tr key={index}>
                        <td>{index}</td>
                        <td>{item.p1}</td>
                        <td>{item.p2}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </Table>
            </div>
          )}
        </div>
      );
    }
  };

  const mainForm = () => {
    return (
      <div>
        <Container fluid>
          <Row>
            <Col>
              <h1 className="text-center">**{appstate}**</h1>
            </Col>
          </Row>
        </Container>

        <hr className="border-bottom solid 2px"></hr>

        <Container fluid className="border">
          <Row>
            <Col xs={4} className="border-right">
              <Form.Label className="form-label">Upload XMI</Form.Label>
              <Form.Control
                type="file"
                name="file"
                accept=".xmi"
                placeholder="choose a file"
                onChange={handleChange("file")}
              />
            </Col>
            <Col xs={4} className="border-right">
              <Button
                className="ml-5 mt-2"
                variant="success"
                disabled={pv_disabled}
                onClick={onSubmitFile}
              >
                Generate Parameters and Values
              </Button>
            </Col>
            <Col xs={4} className="border-right">
              <ExportCSV
                csvData={CSV}
                fileName={"sample"}
                disability={test_case_disabled}
              />
              <Button
                as={Link}
                className="mt-2 mx-5"
                to="/fileup"
                variant="dark"
              >
                Generate Test Cases
              </Button>
            </Col>
          </Row>
        </Container>

        <hr className="border-bottom solid 2px"></hr>

        <Container fluid>
          {error && (
            <Alert variant="danger">
              Error in Generating Parameters and Values
            </Alert>
          )}
          {success && (
            <Alert variant="success">
              Parameters and Values Generated Successfully
            </Alert>
          )}
        </Container>
      </div>
    );
  };

  //TODO: main component
  return (
    <div>
      {mainForm()}
      {pvPrinter()}
    </div>
  );
};

export default App;
