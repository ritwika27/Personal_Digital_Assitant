// calendar.js

window.addEventListener('load', initializeListeners);
function initializeListeners() {
    document.querySelector("#week-select div:first-child").onclick = () => changeWeek(-1);
    document.querySelector("#week-select div:last-child").onclick = () => changeWeek(1);
    document.getElementById("currentText").onclick = openWeekSelector;
    document.getElementById("addEvent").onclick =  openAddEventForm;
}

window.addEventListener('load', initializeCalendar);
function initializeCalendar() {
    const now = new Date(Date.now());
    buildCalendar(now);

    layoutTimeMarks();
}

function buildCalendar(date) {
    const calendarBody = document.querySelector("#daygrid > tbody");

    const square = new Date(date);
    // Set the first square to start on the first Sunday
    square.setDate(square.getDate() - square.getDay());
    const monthName = date.toLocaleString('default', { month: 'long' });
    document.getElementById("currentText").textContent = monthName + " " + square.getDate().toString();

    const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const week = document.querySelector("tbody tr");
    while (week.lastChild) week.lastChild.remove();
    for (let day = 1; day <= 7; day++, square.setDate(square.getDate() + 1)) {
        // build a day td with the square dayBuild
        const col = document.createElement("td");
        if (day == 1 || day == 7) col.setAttribute("class", "weekend");
        if (square.toDateString() == (new Date()).toDateString()) col.setAttribute("class", "currentDay")
        week.appendChild(col);

        const header = document.querySelector("#daygrid th:nth-child(" + day.toString() + ")");
        header.textContent = weekdays[day - 1] + " " + square.getDate();

        populateDay(col, square);
    }
}

function changeWeek(dir) {
    const now = new Date(Date.now());
    now.setDate(now.getDate() + (7 * dir));
    buildCalendar(now);

    document.querySelector("#week-select div:first-child").onclick = () => changeWeek(dir - 1);
    document.querySelector("#week-select div:last-child").onclick = () => changeWeek(dir + 1);
}

function dateAsId(dateObj) {
    return (dateObj.getMonth() + 1).toString() + "_" +
           dateObj.getDate().toString();
}

function layoutTimeMarks() {
    const marks = document.getElementById("timeMarks");
    for (let i = 0; i < marks.children.length; i++) {
        marks.children[i].style.top = "calc(100% / 13 * " + i.toString() + " - 10px)";
    }
}

function populateDay(day, date) {
    const eventsToday = data.filter(evt => {
        const d = new Date(Date.parse(evt.time));
        return d.getDate() == date.getDate() &&
               d.getMonth() == date.getMonth() &&
               d.getFullYear() == date.getFullYear();
    });

    for (event of eventsToday) {
        const ele = createEvent(event);
        const time = new Date(Date.parse(event.time));

        const hoursPast = time.getHours() - 7 + (time.getMinutes() / 60);
        ele.style.top = "calc(100% / 13 *" + hoursPast.toString() + ")";
        ele.style.height = "calc(100% / 13 *" + (event.duration / 60).toString() + ")";
        ele.setAttribute("class", "event");
        day.appendChild(ele);
    }
}

function createEvent(data) {
    const ele = document.createElement("div");
    const title = document.createElement("h3");
    title.textContent = data.name;
    ele.addEventListener("click", () => openEventDetails(data));
    ele.appendChild(title);
    return ele;
}

function openEventDetails(data) {
    const container = document.createElement("div");
    container.setAttribute("id", "eventPanel");

    const title = document.createElement("h2");
    title.setAttribute("class", "eventTitle");
    title.textContent = data.name;
    const time = document.createElement("p");
    time.setAttribute("class", "eventTime");
    container.appendChild(title);
    container.appendChild(time);


    const start = new Date(Date.parse(data.time));
    time.textContent = start.toTimeString().split(' ')[0] + " - ";
    start.setHours(start.getHours(), parseInt(data.duration));
    time.textContent += start.toTimeString().split(' ')[0];
    const desc = document.createElement("p");
    desc.setAttribute("class", "eventDetails");
    desc.innerHTML = data.desc;
    container.appendChild(desc);

    const map = document.createElement("a");
    map.setAttribute("href", "");
    map.textContent = data.location;
    time.appendChild(map);

    const links = document.createElement("div");
    links.setAttribute("id", "links");

    const edit = document.createElement("div");
    edit.setAttribute("class", "linkAndQr");
    const details = document.createElement("a");
    details.textContent = "Edit";
    details.href = "#";
    details.onclick = () => openUpdateEventForm(data);
    edit.appendChild(details);
    links.appendChild(edit);

    container.appendChild(links);
    popup(container);
}

function popup(content, callback) {
    // Remove shade if it exists already
    const oldShade = document.getElementById("curtain");
    if (oldShade) oldShade.remove();

    const shade = document.createElement("div");
    shade.setAttribute("id", "curtain");
    if (callback) shade.onclick = callback;
    else shade.onclick = () => document.getElementById("curtain").remove();

    const popupBox = document.createElement("div");
    popupBox.setAttribute("id", "stage");
    // Prevent clicking the popup box from closing the box; only the curtain
    popupBox.onclick = (evt) => evt.stopPropagation();
    popupBox.appendChild(content);
    shade.appendChild(popupBox);

    const xOut = document.createElement("div");
    xOut.setAttribute("id", "popoutExit");
    shade.appendChild(xOut);

    document.getElementById("viewport").appendChild(shade);
}

function openWeekSelector() {
    const fill = document.createTextNode("Week selection not implemented. Imagine one of those calendar selectors.");
    popup(fill);
}

function openAddEventForm() {
    const shell = document.createElement("div");
    shell.innerHTML = `
        <form id="addEventForm">
            <span>
                <label for="eventName">Event Name</label>
                <input id="eventName" name="title" value="" required>
            </span>
            <span>
                <label for="startTime">Start Time</label>
                <input id="startTime" name="start" type="datetime-local" value="${new Date().toISOString().slice(0, 16)}" required>
            </span>
            <span>
                <label for="endTime">End Time</label>
                <input id="endTime" name="end" type="datetime-local" value="${new Date().toISOString().slice(0, 16)}" required>
            </span>
            <span>
                <label for="location">Location</label>
                <input id="location" name="address" value="" required>
            </span>
            <span>
                <label for="description">Description</label>
                <br />
                <textarea id="description" name="description" rows="5"></textarea>
            </span>
            <input type="submit" value="Add Event" formaction="/addEvent"></input>
        </form>
    `;
    popup(shell);
}


function openUpdateEventForm(data) {
    const shell = document.createElement("div");
		let initial = {}
		if(data){
			initial = {
				"id": data.id || "",
				"name": data.name || "",
				"time": data.time || "",
				"duration": data.duration || "",
				"location": data.location || "",
				"desc": data.desc || ""
			}
		}
    shell.innerHTML = `
        <form id="addEventForm">
            <span>
                <label for="eventName">Event Name</label>
                <input id="eventName" name="title" value="${initial.name}" required>
            </span>
            <span>
                <label for="startTime">Start Time</label>
                <input id="startTime" name="start" type="datetime-local" value="${(initial.time ? new Date(initial.time) : new Date()).toISOString().slice(0, 16)}" required>
            </span>
            <span>
                <label for="endTime">End Time</label>
                <input id="endTime" name="end" type="datetime-local" value="${(initial.time ? (new Date(Date.parse(initial.time) + 60000 * initial.duration)) : (new Date())).toISOString().slice(0, 16)}" required>
            </span>
            <span>
                <label for="location">Location</label>
                <input id="location" name="address" value="${initial.location}" required>
            </span>
            <span>
                <label for="description">Description</label>
                <br />
                <textarea id="description" name="description" rows="5">${initial.desc}</textarea>
            </span>
            <input type="hidden" id="eventId" name="eventId" value="${initial.id}">
            <input type="submit" formaction="/deleteEvent" value="Delete"/>
            <input type="submit" formaction="/updateEvent" value="Update"></input>
        </form>
    `;
    popup(shell);
}


function showNotification(notificationText) {
    const fill = document.createTextNode(notificationText);
    popup(fill);
}
