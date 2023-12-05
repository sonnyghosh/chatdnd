import "./PartyContainer.css"
export const PartyContainer = (PartyMembers) => {
    const { partyList } = PartyMembers;
    const numPartyList = partyList.length;  
    return (
        <div className="border border-red-950 overflow-y-auto text-white font-custom bg-slate-800 h-80 w-96 rounded-md">
            <div className={`grid grid-cols-3 grid-rows-${numPartyList} gap-1 place-items-center mt-2 mb-2`}>
                {partyList.map(member => (
                    <>
                        <img src={ member.profile_picture } className="h-12 w-12 justify-center items-center grid"/>
                        <div className="inline-flex flex-col flex-auto">
                            <p>Name: { member.name }</p>
                            <p>Level: {member.level }</p>
                            <p>Class: { member.gameClass }</p> 
                        </div>
                        <div className="inline-flex flex-col flex-auto">
                            <p>HP: { member.HP }</p>
                            <p>MP: { member.MP }</p>
                            <p>STA: { member.STA }</p>
                        </div>
                    </>                        
                    ))}
            </div>
        </div>
    )
}