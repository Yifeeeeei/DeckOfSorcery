const configs = {
    guide: {
        name: "游玩指南",
        id: "guide",

        function: function () {
            toggleSubMenu("guide-submenu"); // Toggle sub-items for this menu
        },
        subItems: {
            deckBuild: {
                name: "卡组构筑",
                function: function () {
                    jumpToOther("https://yifeeeeei.github.io/ArcaneComposer/");
                },
            },
            ttsMod: {
                name: "TTS模组",
                function: function () {
                    jumpToOther(
                        "https://steamcommunity.com/sharedfiles/filedetails/?id=3155709993"
                    );
                },
            },
        },
    },
    story: {
        name: "背景故事",
        id: "story",
        function: function () {
            toggleSubMenu("story-submenu"); // Toggle sub-items for this menu
        },
        subItems: {
            mermaid: {
                name: "人鱼的故事",
                function: function () {
                    jumpHere("htmls/Mermaid.html");
                },
            },
            Fire: {
                name: "烈火之门派",
                function: function () {
                    jumpHere("htmls/Fires.html");
                },
            },
            Dawn: {
                name: "破晓",
                function: function () {
                    jumpHere("htmls/Dawn.html");
                },
            },
            Storm: {
                name: "风暴之城",
                function: function () {
                    jumpHere("htmls/Storm.html");
                },
            },
        },
    },
};

var baseDiv;
var frameDiv;
function showBase() {
    baseDiv.style.display = "block";
    frameDiv.style.display = "none";
}

function showFrame() {
    baseDiv.style.display = "none";
    frameDiv.style.display = "block";
}

function init() {
    baseDiv = document.getElementById("base");
    frameDiv = document.getElementById("frame");
    console.log(baseDiv);
    console.log(frameDiv);
    showBase();
    prepareMenuItems();
}

function loadFrame(path) {
    var frame = document.getElementById("iframe");
    frame.src = path;
    showFrame();
    console.log("load frame: " + path + frame.src);
}

function jumpToOther(path) {
    // open path in new tab
    window.open(path, "_blank");
}

function jumpHere(path) {
    // open path in current tab
    window.location.href = path;
}

function backToBase() {
    showBase();
}

function prepareMenuItems() {
    // id: {name: function:, subItems: {}}

    const baseMenu = document.getElementById("base-menu");

    // Create menu items
    for (const key in configs) {
        const item = document.createElement("ul");
        item.classList.add("menu-item");
        item.innerHTML = configs[key].name;
        item.onclick = configs[key].function;
        item.id = configs[key].id;
        baseMenu.appendChild(item);

        // If there are sub-items, create a submenu
        if (configs[key].subItems) {
            const subMenu = document.createElement("ul");
            subMenu.id = `${key}-submenu`;
            subMenu.classList.add("submenu");

            for (const subKey in configs[key].subItems) {
                const subItem = document.createElement("li");
                subItem.classList.add("menu-subitem");
                subItem.innerHTML = configs[key].subItems[subKey].name;
                subItem.onclick = configs[key].subItems[subKey].function;
                subMenu.appendChild(subItem);
            }
            item.appendChild(subMenu);
        }
    }
}

function toggleSubMenu(subMenuId) {
    const subMenu = document.getElementById(subMenuId);
    if (subMenu.classList.contains("show")) {
        subMenu.classList.remove("show"); // Hide submenu
    } else {
        subMenu.classList.add("show"); // Show submenu
    }
}
init();
