import React from 'react';

function CustomDatePicker ({ texttoshow, DateValue, setDateValue }) {
  
  return (
    <div className="custom-date-picker flex flex-col gap-2">
      <label htmlFor="date">{texttoshow}:</label>
      {/* Input field for date selection */}
      <input
        className='p-1 rounded-lg border'
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
