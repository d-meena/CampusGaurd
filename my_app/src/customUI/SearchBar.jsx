import React from "react";
import CustomButton from "./CustomButton";
import Datepicker from "./CustomDatePicker"

const SearchBar = ({ onClick, searchNo, setSearchNo, startDate, setStartDate, endDate, setEndDate }) => {
  return (
    <div>
      <input
        className="p-2 rounded-md text-lg w-72 uppercase"
        type="text"
        value={searchNo}
        onChange={(e) => setSearchNo(e.target.value.toUpperCase ? e.target.value.toUpperCase() : e.target.value)}

      />
      <Datepicker 
        texttoshow={ "Start Date"}
        Datevalue = {startDate}
        setDateValue = {setStartDate}
      ></Datepicker>
      <Datepicker
        texttoshow={ "End Date"}
        Datevalue = {endDate}
        setDateValue = {setEndDate}
        ></Datepicker>
      <CustomButton onClick={onClick} customClasses="grow">
        Search
      </CustomButton>
    </div>
  );
};

export default SearchBar;
