import React from 'react';

function CustomDatePicker ({ texttoshow, DateValue, setDateValue }) {
  
  return (
    <div className="custom-date-picker">
      <label htmlFor="date">{texttoshow}:</label>
      {/* Input field for date selection */}
      <input
        type="date"
        id="date"
        name="date"
        value={DateValue}
        onChange={(e) => setDateValue(e.target.value)}
      />
    </div>
  );
}

export default CustomDatePicker;
