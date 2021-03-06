import React from "react";
import { Alert } from "reactstrap";
import "../styles/OptionsTable.css";

const useSortableData = (items = [], config = null) => {
  const [sortConfig, setSortConfig] = React.useState(config);
  const sortedItems = React.useMemo(() => {
    let sortableItems = [...items];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [items, sortConfig]);

  const requestSort = (key) => {
    let direction = "ascending";
    if (
      sortConfig &&
      sortConfig.key === key &&
      sortConfig.direction === "ascending"
    ) {
      direction = "descending";
    }
    setSortConfig({ key, direction });
  };

  return { items: sortedItems, requestSort, sortConfig };
};

const OptionsTable = (props) => {
  const { date, data } = props;
  const { items, requestSort, sortConfig } = useSortableData(data);
  const getClassNamesFor = (name) => {
    if (!sortConfig) {
      return;
    }
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };

  if (data == undefined) {
    return <Alert color="primary">Options do not exist for {date}</Alert>;
  }

  return (
    <table>
      <caption className="Caption">Options for {date}</caption>
      <thead>
        <tr>
          <th>
            <button
              type="button"
              onClick={() => requestSort("name")}
              className={getClassNamesFor("name")}
            >
              Name
            </button>
          </th>
          <th>
            <button
              type="button"
              onClick={() => requestSort("strike")}
              className={getClassNamesFor("strike")}
            >
              Strike Price
            </button>
          </th>
          <th>
            <button
              type="button"
              onClick={() => requestSort("expiry")}
              className={getClassNamesFor("expiry")}
            >
              Expiry
            </button>
          </th>
          <th>
            <button
              type="button"
              onClick={() => requestSort("quantity")}
              className={getClassNamesFor("quantity")}
            >
              Quantity
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.name}>
            <td>{item.name}</td>
            <td>${item.strike}</td>
            <td>{item.expiry}</td>
            <td>{item.quantity}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default OptionsTable;
