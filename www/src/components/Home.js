import React from "react";
import { Input, Label, FormGroup } from "reactstrap";
import { getOptions } from "../api/Options";
import CustomButton from "./CustomButton";
import OptionsTable from "./OptionsTable";

import "../styles/Home.css";

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
  const [optionsData, setOptionsData] = React.useState("");
  const fetchOptionsData = async (date) => {
    date = date.length === 0 ? getCurrentDate() : date;
    const data = await getOptions(date);
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
            fetchOptionsData(date);
          }}
        />
      </div>
      <div className="ResultsContainer">
        <div className="OptionsTable">
          {optionsData && <OptionsTable date={date} data={optionsData.data} />}
        </div>
      </div>
    </div>
  );
}

export default Home;
