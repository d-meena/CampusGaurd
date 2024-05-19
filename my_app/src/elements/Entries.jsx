import axios from "axios";
import React, { useEffect, useState } from "react";
import ReactPaginate from "react-paginate";
import CustomTable from "../customUI/CustomTable";
import SearchBar from "../customUI/SearchBar";
import moment from "moment";
import CustomButton from "../customUI/CustomButton";
// import CustomPagination from "../customUI/CustomPagination";

const BASE_URL = process.env.REACT_APP_BASE_URL;
function Entries() {
  console.log("running"); // why this is logging 4 times?
  const [searchNo, setSearchNo] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const limit = 7;
  const offset = (page - 1) * limit;
  // console.log(offset);
  useEffect(() => {
    axios
      .get(`${BASE_URL}/entries`, {
        params: {
          page: page,
          limit: limit,
          vehicle_no: searchNo,
          startDateISO:
            startDate !== null ? moment(startDate).toISOString() : null,
          endDateISO: endDate !== null ? moment(endDate).toISOString() : null,
        },
      })
      .then((res) => {
        setData(res.data.result);
        setTotalPages(res.data.totalPages);
      })
      .catch((err) => console.log(err));
  }, [page]);
  const [data, setData] = useState([]);

  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const handlePageClick = (event) => {
    setPage(event.selected + 1);
  };

  function handleSearch(e) {
    e.preventDefault();
    console.log("handling Search");
    console.log(searchNo, " searchNo");
    console.log(startDate, " ", endDate);
    axios
      .get(`${BASE_URL}/entries`, {
        params: {
          page: 1,
          limit: limit,
          vehicle_no: searchNo,
          startDateISO:
            startDate !== null ? moment(startDate).toISOString() : null,
          endDateISO: endDate !== null ? moment(endDate).toISOString() : null,
        },
      })
      .then((res) => {
        setData(res.data.result);
        setTotalPages(res.data.totalPages);
      })
      .catch((err) => console.log(err));
  }

  return (
    <>
      <div className="fixed inset-0 h-screen w-full bg-home bg-cover bg-center bg-no-repeat -z-10"></div>
      <div className="flex flex-col gap-4 items-center ">
        <h2 className="p-4">Entries of the Vehicle</h2>
        <SearchBar
          onClick={handleSearch}
          searchNo={searchNo}
          setSearchNo={setSearchNo}
          startDate={startDate}
          setStartDate={setStartDate}
          endDate={endDate}
          setEndDate={setEndDate}
        />
        <CustomTable data={data} offset={offset}></CustomTable>
        <ReactPaginate
          className="flex flex-row gap-3 list-none m-4 items-center"
          activeLinkClassName="active-page-number"
          pageLinkClassName="page-number"
          breakLabel="..."
          pageRangeDisplayed={2}
          onPageChange={handlePageClick}
          pageCount={totalPages}
          previousLabel={<CustomButton> Prev</CustomButton>}
          nextLabel={<CustomButton>Next</CustomButton>}
        />
        {/* <CustomPagination totalPages={totalPages} /> */}
      </div>
    </>
  );
}

export default Entries;
