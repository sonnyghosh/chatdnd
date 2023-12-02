export const PartyContainer = (PartyMembers) => {
    const { partyList } = PartyMembers;
    console.log( partyList ); 
    return (
        <div className="border border-red-950 overflow-y-auto text-white font-custom bg-slate-800 h-80 w-96 rounded-md">
            <div className="grid grid-cols-3">
                {partyList.map(member => (
                    <div key={member.id} className="">
                    </div> 
            ))}
            </div>
        </div>
            
     






















