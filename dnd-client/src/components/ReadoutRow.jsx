import React from "react";

export const ReadoutRow = () => {
    return (
        <div className="flex flex-auto justify-between w-2/3 h-80">
            <EnvironmentContainer />
            <InventoryContainer />
            <PartyContainer />
        </div>
    )
}

function EnvironmentContainer() {

}

function InventoryContainer() {
    const inventoryResponse = {
        gold : 150,
        gems : 50,
        crystals : 20
    }
    const {gold, gem, crystals} = inventoryResponse;
    return (
        <div className="flex flex-col w-1/3 bg-slate-800 border border-red-800">
            <div className="flex flex-row"></div>
            <div className="flex flex-row"></div>
            <div className="flex flex-row"></div>
        </div>
    )
}

function PartyContainer() {

}