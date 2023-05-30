"use strict";

//import span_tree from "./spanning_tree.json"

const nodeCentralDiff = 25;

let root = null;
let svgElement_element = null;
let selectElement = null;

let dragingNode = null;
let className = null;

let lineSVGelements = null;

let choosen_key = null;

window.addEventListener("DOMContentLoaded", (e) => {
    console.log("Contenct loaded!");
    console.log("enbeded_data: ", enbeded_data);

    root = document.getElementById("root");
    if (!root) console.log("No root div found!!!");

    root.insertAdjacentHTML(`beforeend`, startNodeOption());
    root.insertAdjacentHTML(`beforeend`, svgElement());
    svgElement_element = root.querySelector(".svg_frame");

    selectElement = root.querySelector("select");
    selectElement.addEventListener("change", setChoosenNode);
});

function setChoosenNode(event) {
    choosen_key = event.target.value;
    let allNodeElement = root.querySelectorAll("p");
    allNodeElement.forEach((el) => el.remove());

    svgElement_element.innerHTML = "";

    if (choosen_key != "") {
        iterateNodeFiles();
        changePosition();
    }
}

function changePosition() {
    const all_nodes = root.querySelectorAll("p");

    all_nodes.forEach((node) => {
        node.addEventListener("mousedown", catchElement)

        node.addEventListener("mouseover", (event) => {
            const p_increase = "p_increase"
            const p_deincrease = "p_deincrease"
            event.target.classList.remove(p_deincrease)
            event.target.classList.add(p_increase)

        })
        node.addEventListener("mouseleave", (event) => {
            const p_increase = "p_increase"
            const p_deincrease = "p_deincrease"
            event.target.classList.remove(p_increase)
            event.target.classList.add(p_deincrease)

        })
    });
    root.addEventListener("mousemove", moveElement);
    root.addEventListener("mouseup", mouseLeaveElement);
}

let mousePosition = { x: undefined, y: undefined };
let offsets = { x: undefined, y: undefined };

let isMouseStartHold = false;

let allClassNameSellected = null;

function catchElement(ev) {
    mousePosition.x = ev.clientX;
    mousePosition.y = ev.clientY;

    dragingNode = ev.target;

    offsets.x = dragingNode.getBoundingClientRect().x - mousePosition.x;
    offsets.y = dragingNode.getBoundingClientRect().y - mousePosition.y;

    className = ev.target.classList[0];
    ev.target.style.cursor = "grabbing"

    allClassNameSellected = Object.entries(lineSVGelements).filter(([index, item]) => item.classList.value.includes(className));

    isMouseStartHold = true;
}

function moveElement(ev) {
    if (isMouseStartHold) {
        mousePosition.x = ev.clientX;
        mousePosition.y = ev.clientY;

        let newX = mousePosition.x + offsets.x;
        let newY = mousePosition.y + offsets.y;

        dragingNode.style.left = `${newX}px`;
        dragingNode.style.top = `${newY}px`;

        allClassNameSellected.forEach(([_, item]) => {
            let classListValue = item.classList.value;
            let splitedClassName = classListValue.split("");

            if (splitedClassName.includes(className)) {
                let [start, end] = splitedClassName;
                if (start === className) {
                    item.setAttribute("x1", newX + nodeCentralDiff);
                    item.setAttribute("y1", newY + nodeCentralDiff);
                }

                if (end === className) {
                    item.setAttribute("x2", newX + nodeCentralDiff);
                    item.setAttribute("y2", newY + nodeCentralDiff);
                }
            }
        });
    }
}

function mouseLeaveElement(ev) {
    if (isMouseStartHold) {
        isMouseStartHold = false;
        ev.target.style.cursor = "grab"
    }
}

function draw_one_tree(key_coord_pair) {
    let nodeClassSet = new Set();
    let lineStringArray = [];

    const choosen_tree = Object.entries(enbeded_data).find(([key, tree_arr]) => key === choosen_key);

    choosen_tree[1].forEach((node_link_array) => {
        node_link_array.forEach((current_node, index) => {
            let nextNode = node_link_array[index + 1];
            if (!nextNode) return;

            let nodePair = current_node + nextNode;
            if (nodeClassSet.has(nodePair)) return;

            let coords = key_coord_pair[current_node];
            let origin_coords = coords;
            let dest_coords = key_coord_pair[nextNode];

            if (!dest_coords) dest_coords = origin_coords;

            let line = drawConnectionLine(nodePair, origin_coords["x"], origin_coords["y"], dest_coords["x"], dest_coords["y"]);
            lineStringArray.push(line);

            nodeClassSet.add(nodePair);
        });
    });

    svgElement_element.insertAdjacentHTML(`beforeend`, lineStringArray.join(""));

    lineSVGelements = svgElement_element.querySelectorAll("line");
}

function addNodeToPage(node_t, f_x, f_y, endLine_x, endLine_y) {
    const node = getPointElement(node_t, f_x, f_y);
    root.insertAdjacentHTML(`beforeend`, node);
}

function iterateNodeFiles() {
    let key_coord_pair = {};
    
    const fix_points = NODE_FIX_POINTS()
    Object.entries(fix_points).forEach(([key, data], index) => {
        if (!enbeded_data[key]) return

        key_coord_pair[key] = { x: data.x, y: data.y };
        addNodeToPage(key, data.x, data.y, data.x, data.y);
    });
    
    draw_one_tree(key_coord_pair);
    
    // region------RANDOM NODES----
    
        //const randomCoord = () => Math.floor(Math.random() * 680 + 100);
        // Object.entries(data).forEach(([key, data], index) => {
        //     let f_x = randomCoord();
        //     let f_y = randomCoord();
        //     key_coord_pair[key] = { x: f_x, y: f_y };
        //     addNodeToPage(key, f_x, f_y, f_x, f_y);
        // });
        // draw_one_tree(key_coord_pair);
    
    // endregion
}
 
//----------VIEW ELEMENTS-----------------
function startNodeOption() {
    let optionsArray = [];

    Object.keys(enbeded_data).forEach((key) => {
        optionsArray.push(`<option value='${key}'>${key}</option>`);
    });

    return `<div class="node_choose">
                <label for="pet-select">Node-k listája:</label>
                <select name="pets" id="pet-select">
                    <option value="">--Válassz!--</option>
                    ${optionsArray.join("")}
                </select>
            </div>`;
}

function svgElement() {
    return `<svg class="svg_frame"  width="100%" height="100%"> </svg>`;
}

function drawConnectionLine(className, from_x, from_y, to_x, to_y) {
    return `<line class="${className}" x1="${from_x}" y1="${from_y}" x2="${to_x}" y2="${to_y}" style="position: absolute;" />`;
}

function getPointElement(node_name, x_coord, y_coord) {
    if (!node_name) node_name = "missing!";
    return `<p class="${node_name}" style="left: calc(${x_coord}px - ${nodeCentralDiff}px); top: calc(${y_coord}px - ${nodeCentralDiff}px);">${node_name}</p>`;
}

function NODE_FIX_POINTS() {
    return {
        B: { x: 353, y: 173 },
        S: { x: 211, y: 295 },
        C: { x: 403, y: 331 },
        D: { x: 582, y: 323 },
        E: { x: 549, y: 564 },
        F: { x: 324, y: 629 },
        G: { x: 217, y: 476 },
        H: { x: 555, y: 160 },
        I: { x: 393, y: 468 },
    };
}
