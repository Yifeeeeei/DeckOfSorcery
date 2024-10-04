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
    var frame = document.getElementById("frame");
    frame.src = path;
    showFrame();
}

function jumpToOther(path) {
    // open path in new tab
    window.open(path, "_blank");
}

function backToBase() {
    showBase();
}

function prepareMenuItems() {
    // id: {name: function:}
    configs = {
        "build-your-deck": {
            name: "构筑卡组",
            function: function () {
                jumpToOther("https://yifeeeeei.github.io/SorceryComposer/");
            },
        },
        story: {
            name: "故事:巴特尔",
            function: function () {
                loadFrame("1.html");
            },
        },
    };

    // add to base menu
    var baseMenu = document.getElementById("base-menu");
    for (var key in configs) {
        var item = document.createElement("ul");
        item.classList.add("menu-item");
        item.innerHTML = configs[key].name;
        item.onclick = configs[key].function;
        baseMenu.appendChild(item);
        console.log(item);
    }
}

init();
