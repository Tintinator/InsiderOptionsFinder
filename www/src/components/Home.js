import React from "react";
import "../styles/Home.css";
import CustomButton from "./CustomButton";
import { Input, Label, FormGroup } from "reactstrap";
import { getOptions } from "../api/Options";

function getCurrentDate() {
  var dt = new Date();
  var year = dt.getFullYear();
  var month = (dt.getMonth() + 1).toString().padStart(2, "0");
  var day = dt.getDate().toString().padStart(2, "0");
  var res = year + "-" + month + "-" + day;
  return res;
}

function Home() {
  const [date, setDate] = React.useState("");
  const [isLoaded, setIsLoaded] = React.useState("");
  const [optionsData, setOptionsData] = React.useState("");
  const fetchOptionsData = async (date) => {
    const data = await getOptions(date);
    console.log(data);
    setOptionsData(data);
  };

  return (
    <div className="Home">
      <div className="DateEntryContainer">
        <CustomButton
          name="Today's Date"
          onClickHandler={() => {
            // set date as YYYY-MM-DD
            setDate(getCurrentDate);
          }}
        />
        <div>or</div>
        <FormGroup>
          <Label for="exampleEmail">Set Custom Date</Label>
          <Input
            type="date"
            name="customDate"
            placeholder="choose a date"
            onChange={(e) => {
              setDate(e.target.value);
            }}
            value={date}
          />
        </FormGroup>
        <CustomButton
          name="Search"
          onClickHandler={() => {
            fetchOptionsData();
          }}
        />
      </div>
      <div className="ResultsContainer">asdf</div>
    </div>
  );
}

export default Home;