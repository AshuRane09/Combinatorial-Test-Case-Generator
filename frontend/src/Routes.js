import React from "react";
import { Switch, BrowserRouter as Router, Route } from "react-router-dom";
import App from "./App";
import Home from "./Home";
import FileUpload from "./fileupload";

const Routes = () => {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/parser" exact component={App} />
        <Route path="/fileup" exact component={FileUpload} />
      </Switch>
    </Router>
  );
};

export default Routes;
