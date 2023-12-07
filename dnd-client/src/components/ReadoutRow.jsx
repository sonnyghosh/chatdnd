import React from "react";
import { InventoryContainer } from ".";
import { PartyContainer } from ".";

export const ReadoutRow = () => {
    return (
        <div className="flex flex-auto justify-between w-2/3 h-80">
            <EnvironmentContainer />
            <InventoryContainer />
            <PartyContainer />
        </div>
    )
}

function EnvironmentContainer(imgSrc) {
    return (
        <div className="h-80 rounded-md border">
            <img src={imgSrc} />
        </div>
    )
}