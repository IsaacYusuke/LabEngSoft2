import React from "react";
import { ReactComponent as LogoBlack } from '../../assets/apollo-logo-black.svg';
import { ReactComponent as LogoGrad } from '../../assets/apollo-logo.svg';

function Logo(props) {
    const classes = "logo " + props.className;

    return (
        <div className={classes}>
            {
                classes.includes("black")
                ? <LogoBlack />
                : <LogoGrad />
            }
        </div>
    );
}

export default Logo;
