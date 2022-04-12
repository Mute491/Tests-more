const playFieldColoumns = 25;
const playFieldLines = 25;
let snake = ["13-13"];

let isAlive = true;
let direction = "up";
let points = 0;

let pointsCoordinates = Math.floor((Math.random() * (playFieldColoumns-11))+11)+"-"+Math.floor((Math.random() * (playFieldLines-11))+11);



function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
}

document.getElementById("gioca").addEventListener("click", ()=>{

  document.getElementById("startgamescreen").style.display = "none";
  document.getElementById("playgroundcontainer").style.visibility = "visible";
  main();

});

document.addEventListener('keypress', changedirection);

function changedirection(e) {

  if(e.code === "KeyW"){

    direction = "up";

  }
  else if (e.code === "KeyS") {

    direction = "down";

  }
  else if(e.code === "KeyD"){

    direction = "right";

  }
  else if (e.code === "KeyA") {

    direction = "left";

  }

}


function generate_table(){

  // creates a <table> element and a <tbody> element
  var tbl = document.getElementById("playfield");
  var tblBody = document.createElement("tbody");

  // creating all cells
  for (var i = 10; i < playFieldLines; i++) {
    // creates a table row
    var row = document.createElement("tr");

    for (var j = 10; j < playFieldLines; j++) {
      // Create a <td> element and a text node, make the text
      // node the contents of the <td>, and put the <td> at
      // the end of the table row
      var cell = document.createElement("td");
      var image = document.createElement("img");
      image.id=(i+1)+"-"+(j+1);
      cell.appendChild(image);
      row.appendChild(cell);
    }

    // add the row to the end of the table body
    tblBody.appendChild(row);
  }

  // put the <tbody> in the <table>
  tbl.appendChild(tblBody);
}


function addlength(){

  let len = snake.length;

  let line = parseInt(snake[len-1].charAt(3)+""+snake[len-1].charAt(4));
  let coloumn = parseInt(snake[len-1].charAt(0)+""+snake[len-1].charAt(1));

  if(direction === "up"){

    if((line-1) === 10){

      coloumn--;

    }
    else{

      line--;

    }

  }
  else if(direction === "left"){

    if((coloumn-1) === 10){

      line--;

    }
    else{

      coloumn--;

    }

  }
  else if (direction === "right") {

    if((line+1) === (playFieldColoumns+1)){

      line++;

    }
    else{

      coloumn++;

    }

  }
  else{

    if((line+1) === (playFieldLines+1)){

      coloumn++;

    }
    else{

      line++;

    }

  }

  snake.push(coloumn+"-"+line);

}



function move(){

  let line = parseInt(snake[0].charAt(3)+""+snake[0].charAt(4));
  let coloumn = parseInt(snake[0].charAt(0)+""+snake[0].charAt(1));



  if(direction === "up"){

    coloumn--;

  }

  else if(direction === "down"){

    coloumn++;

  }

  else if(direction === "left"){

    line--;

  }
  else{

    line++;

  }

  if(coloumn === 10 || line === 10 || coloumn === (playFieldColoumns+1) || line === (playFieldLines+1)){

    isAlive = false;
    return;

  }
  else if(snake.indexOf(coloumn+"-"+line)>-1){

    isAlive = false;

    return;

  }


  snake.unshift(coloumn+"-"+line);
  snake.pop();

}



function refreshsnake(){

  let len = snake.length;

  for(let i=0; i<len; i++){

    document.getElementById(snake[i]).src = "";
    document.getElementById(snake[i]).style.visibility = "hidden";

  }

  move();

  for(let i=0; i<len; i++){

    document.getElementById(snake[i]).src = "img/square.png";
    document.getElementById(snake[i]).style.visibility = "visible";

  }

}



function pointcollected(){

    points += 100;
    addlength();

    document.getElementById(pointsCoordinates).src = "";
    document.getElementById(pointsCoordinates).style.visibility = "hidden";

    do{

      pointsCoordinates = Math.floor((Math.random() * (playFieldColoumns-11))+11)+"-"+Math.floor((Math.random() * (playFieldLines-11))+11);

    }while(snake.indexOf(pointsCoordinates)>-1);

    document.getElementById(pointsCoordinates).src = "img/apple.png";
    document.getElementById(pointsCoordinates).style.visibility = "visible";

    document.getElementById("score").innerHTML = "punteggio: "+points;

}



async function main(){

  generate_table();

  document.getElementById(snake[0]).src = "img/square.png";
  document.getElementById(snake[0]).style.visibility = "visible";
  document.getElementById(pointsCoordinates).src = "img/apple.png";
  document.getElementById(pointsCoordinates).style.visibility = "visible";

  while(isAlive){

    await sleep(300);
    refreshsnake();

    if(snake[0] === pointsCoordinates){

      pointcollected();

    }

  }

  document.getElementById("gameover").style.visibility = "visible";
  document.getElementById("playgroundcontainer").style.display = "none";
  document.getElementById("endgamescreen").style.display = "inline";

  document.getElementById("showscore").value = points;

}
