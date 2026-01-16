import streamlit as st
from utils import inject_css
from game.utils import Duel, Parzival, Gawan, Feirefiz, Cundrie, Orgeluse, Arthur

# Initialize characters in session state so they persist across reruns
if "characters" not in st.session_state:
    st.session_state.characters = {
        "Parzival": Parzival(),
        "Gawan": Gawan(),
        "Feirefiz": Feirefiz(),
        "Cundrie la Surziere": Cundrie(),
        "Orgeluse": Orgeluse(),
        "King Arthur": Arthur()
    }

inject_css()

# SCOREBOARD at the top
st.title("⚔️ The Fight for the Grail! ⚔️")
st.header("🏆 Scoreboard - Honor Rankings")

# Create scoreboard with character stats
scoreboard_data = []
for name, char in st.session_state.characters.items():
    scoreboard_data.append({
        "Character": name,
        "Honor": char.honor,
        "Diplomacy": char.traits["Diplomacy"],
        "Martial": char.traits["Martial"],
        "Stewardship": char.traits["Stewardship"],
        "Intrigue": char.traits["Intrigue"],
        "Learning": char.traits["Learning"]
    })

# Sort by honor (descending)
scoreboard_data.sort(key=lambda x: x["Honor"], reverse=True)

# Display scoreboard
for i, data in enumerate(scoreboard_data, 1):
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1, 1, 1, 1])
    with col1:
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        st.write(f"**{medal} {data['Character']}**")
    with col2:
        st.write(f"❤️ {data['Honor']}")
    with col3:
        st.write(f"💬 {data['Diplomacy']}")
    with col4:
        st.write(f"⚔️ {data['Martial']}")
    with col5:
        st.write(f"💰 {data['Stewardship']}")
    with col6:
        st.write(f"🎭 {data['Intrigue']}")
    with col7:
        st.write(f"📚 {data['Learning']}")

st.divider()

# DUEL SETUP
st.header("⚔️ Setup Duel")

characters = list(st.session_state.characters.values())
character_names = list(st.session_state.characters.keys())
traits = ["Diplomacy", "Martial", "Stewardship", "Intrigue", "Learning"]

# Character 1 selection
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fighter 1")
    character1_name = st.selectbox("Pick the first character", character_names, index=None, key="char1")
    character1 = st.session_state.characters[character1_name] if character1_name else None
    
    if character1:
        character1_major = st.selectbox("Pick the major trait", traits, index=None, key="major1")
        character1_minor = st.selectbox("Pick the minor trait", traits, index=None, key="minor1")
        
        # Show special ability info
        st.info(f"**Special:** {character1.special}")
        
        # Special ability selector
        use_char1_ability = False
        char1_ability_detail = None
        
        if character1_name == "Cundrie la Surziere":
            remaining = character1.ability_uses.get("stat_decrease", 0)
            if remaining > 0:
                use_char1_ability = st.checkbox(
                    f"Use Oppressor of Joy? ({remaining} uses left)",
                    key="use_ability1"
                )
                if use_char1_ability:
                    st.success("Will decrease opponent's all stats by 2!")
            else:
                st.warning("No uses of Oppressor of Joy remaining")
                
        elif character1_name == "Orgeluse":
            remaining = character1.ability_uses.get("stat_decrease", 0)
            if remaining > 0:
                use_char1_ability = st.checkbox(
                    f"Use Haughty Maiden? ({remaining} uses left)",
                    key="use_ability1"
                )
                if use_char1_ability:
                    st.success("Will decrease opponent's all stats by 1!")
            else:
                st.warning("No uses of Haughty Maiden remaining")
                
        elif character1_name == "King Arthur":
            available_knights = [k for k, v in character1.ability_uses["knights"].items() if v]
            if available_knights:
                char1_ability_detail = st.selectbox(
                    "Summon a knight from the Round Table?",
                    ["None"] + available_knights,
                    key="knight1"
                )
                if char1_ability_detail != "None":
                    use_char1_ability = True
                    if char1_ability_detail == "Kay":
                        st.success("Will give +3 Martial, -3 Stewardship")
                    elif char1_ability_detail == "Iwein":
                        st.success("Will give +3 Diplomacy, -3 Intrigue")
                    elif char1_ability_detail == "Lanzelet":
                        st.success("Will give +3 Intrigue, -3 Learning")
            else:
                st.warning("All knights have been summoned")
        else:
            # Automatic abilities (Parzival, Gawan, Feirefiz)
            if character1_name == "Parzival":
                remaining = character1.ability_uses.get("minor_ignore", 0)
                st.info(f"Automatic: Ignores minor damage ({remaining} uses left)")
            elif character1_name == "Gawan":
                remaining = character1.ability_uses.get("major_ignore", 0)
                st.info(f"Automatic: Ignores major damage ({remaining} uses left)")
            elif character1_name == "Feirefiz":
                st.info("Automatic: Never takes major damage from Parzival")
    else:
        character1_major = None
        character1_minor = None

with col2:
    st.subheader("Fighter 2")
    character2_name = st.selectbox("Pick the second character", character_names, index=None, key="char2")
    character2 = st.session_state.characters[character2_name] if character2_name else None
    
    if character2:
        character2_major = st.selectbox("Pick the major trait", traits, index=None, key="major2")
        character2_minor = st.selectbox("Pick the minor trait", traits, index=None, key="minor2")
        
        # Show special ability info
        st.info(f"**Special:** {character2.special}")
        
        # Special ability selector
        use_char2_ability = False
        char2_ability_detail = None
        
        if character2_name == "Cundrie la Surziere":
            remaining = character2.ability_uses.get("stat_decrease", 0)
            if remaining > 0:
                use_char2_ability = st.checkbox(
                    f"Use Oppressor of Joy? ({remaining} uses left)",
                    key="use_ability2"
                )
                if use_char2_ability:
                    st.success("Will decrease opponent's all stats by 2!")
            else:
                st.warning("No uses of Oppressor of Joy remaining")
                
        elif character2_name == "Orgeluse":
            remaining = character2.ability_uses.get("stat_decrease", 0)
            if remaining > 0:
                use_char2_ability = st.checkbox(
                    f"Use Haughty Maiden? ({remaining} uses left)",
                    key="use_ability2"
                )
                if use_char2_ability:
                    st.success("Will decrease opponent's all stats by 1!")
            else:
                st.warning("No uses of Haughty Maiden remaining")
                
        elif character2_name == "King Arthur":
            available_knights = [k for k, v in character2.ability_uses["knights"].items() if v]
            if available_knights:
                char2_ability_detail = st.selectbox(
                    "Summon a knight from the Round Table?",
                    ["None"] + available_knights,
                    key="knight2"
                )
                if char2_ability_detail != "None":
                    use_char2_ability = True
                    if char2_ability_detail == "Kay":
                        st.success("Will give +3 Martial, -3 Stewardship")
                    elif char2_ability_detail == "Iwein":
                        st.success("Will give +3 Diplomacy, -3 Intrigue")
                    elif char2_ability_detail == "Lanzelet":
                        st.success("Will give +3 Intrigue, -3 Learning")
            else:
                st.warning("All knights have been summoned")
        else:
            # Automatic abilities (Parzival, Gawan, Feirefiz)
            if character2_name == "Parzival":
                remaining = character2.ability_uses.get("minor_ignore", 0)
                st.info(f"Automatic: Ignores minor damage ({remaining} uses left)")
            elif character2_name == "Gawan":
                remaining = character2.ability_uses.get("major_ignore", 0)
                st.info(f"Automatic: Ignores major damage ({remaining} uses left)")
            elif character2_name == "Feirefiz":
                st.info("Automatic: Never takes major damage from Parzival")
    else:
        character2_major = None
        character2_minor = None

# DUEL BUTTON
if character1 and character2 and character1_major and character1_minor and character2_major and character2_minor:
    if st.button("⚔️ DUEL! ⚔️", type="primary", use_container_width=True):
        st.divider()
        st.header("⚔️ Battle Results")
        
        # Apply pre-duel abilities
        ability_messages = []
        
        # Character 1 abilities
        if use_char1_ability:
            if character1_name == "Cundrie la Surziere":
                character1.use_oppressor(character2)
                ability_messages.append(f"✨ {character1.name} uses Oppressor of Joy!")
            elif character1_name == "Orgeluse":
                character1.use_haughty_maiden(character2)
                ability_messages.append(f"✨ {character1.name} uses Haughty Maiden!")
            elif character1_name == "King Arthur" and char1_ability_detail:
                character1.summon_knight(char1_ability_detail)
                ability_messages.append(f"🗡️ {character1.name} summons Sir {char1_ability_detail}!")
        
        # Character 2 abilities
        if use_char2_ability:
            if character2_name == "Cundrie la Surziere":
                character2.use_oppressor(character1)
                ability_messages.append(f"✨ {character2.name} uses Oppressor of Joy!")
            elif character2_name == "Orgeluse":
                character2.use_haughty_maiden(character1)
                ability_messages.append(f"✨ {character2.name} uses Haughty Maiden!")
            elif character2_name == "King Arthur" and char2_ability_detail:
                character2.summon_knight(char2_ability_detail)
                ability_messages.append(f"🗡️ {character2.name} summons Sir {char2_ability_detail}!")
        
        # Display ability messages
        if ability_messages:
            st.subheader("Pre-Battle Actions")
            for msg in ability_messages:
                st.success(msg)
        
        # Run the duel
        duel = Duel(
            character1=character1, 
            major1=character1_major, 
            minor1=character1_minor,
            character2=character2,
            major2=character2_major,
            minor2=character2_minor
        )
        char1_major_dmg, char1_minor_dmg, char2_major_dmg, char2_minor_dmg = duel.play(verbose=False)
        
        # Display results
        st.subheader("Damage Dealt")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label=f"{character1.name}",
                value=f"{char1_major_dmg + char1_minor_dmg} total damage",
                delta=f"-{char1_major_dmg} major, -{char1_minor_dmg} minor",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                label=f"{character2.name}",
                value=f"{char2_major_dmg + char2_minor_dmg} total damage",
                delta=f"-{char2_major_dmg} major, -{char2_minor_dmg} minor",
                delta_color="inverse"
            )
        
        st.success("Duel complete! Check the scoreboard for updated stats.")
        st.info("💡 Tip: The page will update automatically to show new character stats.")
        
        # Force a rerun to update the scoreboard
        st.rerun()
else:
    if not (character1 and character2):
        st.info("👆 Select both fighters to begin")
    elif not (character1_major and character1_minor and character2_major and character2_minor):
        st.info("👆 Select major and minor traits for both fighters")