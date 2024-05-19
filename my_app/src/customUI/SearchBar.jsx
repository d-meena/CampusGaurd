import React from "react";
import CustomButton from "./CustomButton";
import Datepicker from "./CustomDatePicker"

const SearchBar = ({ onClick, searchNo, setSearchNo, startDate, setStartDate, endDate, setEndDate, className }) => {
  return (
    <div className={`${className ?? ""} flex-row flex justify-between gap-10`}>
      <input
        className="py-2 px-4 rounded-md text-lg w-72 uppercase"
        type="text"
        value={searchNo}
        placeholder="vehicle no."
        onChange={(e) => setSearchNo(e.target.value.toUpperCase ? e.target.value.toUpperCase() : e.target.value)}
      />
      <Datepicker 
        className=""
        texttoshow={"Start Date"}
        Datevalue = {startDate}
        setDateValue = {setStartDate}
      ></Datepicker>
      <Datepicker
        texttoshow={ "End Date"}
        Datevalue = {endDate}
        setDateValue = {setEndDate}
        ></Datepicker>
      <CustomButton onClick={onClick}>
        Search
      </CustomButton>
    </div>
  );
};

export default SearchBar;
