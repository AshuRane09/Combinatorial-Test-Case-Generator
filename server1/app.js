const express = require("express");
const formidable = require("formidable");
const bodyParser = require("body-parser");
const fs = require("fs");
const cors = require("cors");

const fileUpload = require("express-fileupload");
const { spawn } = require("child_process");
const path = require("path");

const app = express();
const { convertXMITOJSON } = require("../server1/scripts");

app.use(express.static("public"));

app.use(bodyParser.json());
app.use(cors());

app.post("/submit", (req, res) => {
  console.log("route visited");
  let form = new formidable.IncomingForm();
  form.keepExtensions = true;
  form.parse(req, (err, fields, files) => {
    if (err) {
      return res.status(400).json({
        error: "error in parsing the file",
      });
    }

    if (files.myfile !== undefined) {
      convertXMITOJSON(files.myfile.path)
        .then((result) => {
          return res.status(200).json(result);
        })
        .catch((err) => console.log("error in getting result!"));
    } else {
      return res.status(400).json({
        error: "error in reading the file",
      });
    }
  });
});

app.get("/", (req, res) => {
  return res.send("hello world!");
});

app.use(fileUpload());

app.post("/upload", (req, res) => {
  if (!req.files) {
    return res.status(500).send({ msg: "file is not found" });
  }
  const myFile = req.files.file;
  myFile.name = "myfile.xlsx";
  myFile.mv(`./${myFile.name}`, function (err) {
    if (err) {
      console.log(err);
      return res.status(500).send({ msg: "Error occured" });
    }
    return res.send({ name: myFile.name, path: `/${myFile.name}` });
  });
});

app.post("/Pairs", (req, res) => {
  const data = JSON.stringify(req.body.Data);
  const process = spawn("python3", ["../pyScript/Pairs.py", data]);
  process.stdout.on("data", (data) => {
    res.send(data);
  });
});

app.get("/download", (req, res) => {
  var file = "Final.csv";
  var fileLocation = path.join("./", file);
  res.download(fileLocation, file);
  // fs.unlinkSync(fileLocation);
});

app.get("/pso", (req, res) => {
  try {
    const process = spawn("python3", ["../pyScript/pso.py"]);
    process.stdout.on("data", (data) => {});
    process.stdout.on("end", function () {
      if (fs.existsSync(path.join("./", "Final.csv"))) {
        try {
          fs.unlinkSync(path.join("./", "result.csv"));
          fs.unlinkSync(path.join("./", "result.txt"));
          fs.unlinkSync(path.join("./", "output.txt"));
          res.status(200).send();
        } catch (e) {
          res.status(400).send();
        }
      } else {
        res.status(400).send();
      }
    });
    process.stdin.end();
  } catch (e) {
    res.status(400).send();
  }
});

app.get("/tlbo", (req, res) => {
  try {
    const process = spawn("python3", ["../pyScript/tlbo.py"]);
    process.stdout.on("data", (data) => {});
    process.stdout.on("end", function () {
      if (fs.existsSync(path.join("./", "Final.csv"))) {
        try {
          fs.unlinkSync(path.join("./", "result.csv"));
          fs.unlinkSync(path.join("./", "result.txt"));
          res.status(200).send();
        } catch (e) {
          res.status(400).send();
        }
      } else {
        res.status(400).send();
      }
    });
    process.stdin.end();
  } catch (e) {
    res.status(400).send();
  }
});

app.get("/sa", (req, res) => {
  try {
    const process = spawn("python3", ["../pyScript/sa.py"]);
    process.stdout.on("data", (data) => {});
    process.stdout.on("end", function () {
      if (fs.existsSync(path.join("./", "Final.csv"))) {
        try {
          fs.unlinkSync(path.join("./", "result.csv"));
          fs.unlinkSync(path.join("./", "result.txt"));
        } catch (e) {
          res.status(400).send();
        }
        res.status(200).send();
      } else {
        res.status(400).send();
      }
    });
    process.stdin.end();
  } catch (e) {
    res.status(400).send();
  }
});

const port = 8000 || process.env.PORT;

app.listen(port, () => {
  console.log("server is running on port ", port);
});
