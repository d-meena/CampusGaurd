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
      className={`${typeStyle} ${customClasses} hover:shadow-xl border-none bg-slate-700 text-white cursor-pointer hover:bg-slate-600`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

export default CustomButton;
