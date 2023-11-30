export const PartyContainer = (PartyMembers) => {
    const { partyList } = PartyMembers;
    return (
        <div className="border border-red-950 flex flex-col flex-auto overflow-y-auto">
            {partyList.map(member => (
                <div key={member.id} className="flex flex-auto flex-row">
                    <div className="flex flex-auto flex-col">
                        <img src={`data:image/png;base64,${ member.profile_picture }`} className="h-12 w-12"/>   
                    </div>
                    <div className="flex flex-auto flex-col">
                        <p> { member.name } </p>
                        <p>Level: { member.level }</p>
                        <p>Class: { member.gameClass }</p>
                    </div>
                    <div className="flex flex-auto flex-col">
                        <p>HP: { member.HP }</p>
                        <p>MP: { member.MP }</p>
                        <p>STA: { memver.STA }</p>
                    </div>
                </div>
            ))}
        </div>
    )
}