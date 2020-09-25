export const getOptions = async function getOptions(date, options = {}) {
  let url = `http://localhost:5000/api/retrieveOptions?inputDate=2020-09-17 ${date}`;
  let failureStatus = null;
  var fakeData = {
    "CorMedix Inc.": [
      ["4.5700", "2030-09-15", "20000.0000"],
      ["4.5700", "2030-09-15", "3750.0000"],
    ],
    data: [
      {
        name: "CorMedix Inc",
        strike: "4.57",
        expiry: "2030-09-15",
        quantity: "20000.0000",
      },
      {
        name: "Test Laboratories Inc",
        strike: "6.9",
        expiry: "2041-09-15",
        quantity: "6900.0000",
      },
    ],
  };

  return fakeData;
  // const response = await fetch(url, options);

  // if (!response.ok) {
  //   failureStatus = response.status;
  // }

  // let data = await response.json();

  // if (failureStatus) {
  //   const error = `${failureStatus}: ${response.statusText}`;
  //   return { data: error, failureStatus };
  // }

  // return { data, failureStatus };
};
