import React, { Component } from "react";
import { Button } from "reactstrap";

class CustomButton extends Component {
  render() {
    const { onClickHandler, name } = this.props;

    return (
      <Button color="primary" onClick={onClickHandler}>
        {name}
      </Button>
    );
  }
}

export default CustomButton;
