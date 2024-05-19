import React from "react";

const CustomButton = ({ onClick, type, children, customClasses }) => {
  let typeStyle;
  switch (type) {
    case 1:
      typeStyle = "text-xl rounded-2xl p-16";
      break;
    default:
      typeStyle = "rounded-md py-3 px-4";
      break;
  }
  return (
    <button
      className={`${typeStyle} ${customClasses} font-bold border-solid bg-slate-700 text-white bg-opacity-90 cursor-pointer hover:bg-slate-600 hover:shadow-2xl border-white border-2`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

export default CustomButton;
