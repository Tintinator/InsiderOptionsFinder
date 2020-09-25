export const getOptions = async function getOptions(date, options = {}) {
  let url = `http://localhost:5000/api/retrieveOptions?inputDate=${date}`;
  console.log(url);
  let failureStatus = null;

  const response = await fetch(url, options);

  // if (!response.ok) {
  //   failureStatus = response.status;
  // }

  let data = await response.json();

  // if (failureStatus) {
  //   const error = `${failureStatus}: ${response.statusText}`;
  //   return { data: error, failureStatus };
  // }

  // return { data, failureStatus };

  return data;
};
