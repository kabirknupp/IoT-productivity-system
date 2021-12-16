

    const formEl = document.querySelector('form')
    const tbodyEl = document.querySelector('tbody');
    const tableEL = document.querySelector('table')


    function onAddWebsite(e) {
        e.preventDefault();
        const difficulty = document.getElementById('difficulty').value;
        const task = document.getElementById('task').value;
        tbodyEl.innerHTML += `
            <tr class="active-row">
                <td>${task}</td>
                <td>${difficulty + '/10'}</td>
                <td><button class="deleteBtn">Finish Task</button></td>
            </tr>
            `;
           // alert(task)
      }

      function onDeleteRow(e){
          if (!e.target.classList.contains('deleteBtn')) {
              return;
          }
          //alert('clicked on button')
          const btn = e.target;
          btn.closest("tr").remove();
          reset(); //reset the timer
          endTask(getTask(), getDifficulty());
          resetTime();
         }

  
    formEl.addEventListener('submit', onAddWebsite);
    tableEL.addEventListener('click', onDeleteRow);


    var difficulty = 0;



function getTask() {
    var nameField = document.getElementById('task').value;
    return nameField
    }


function getDifficulty() {
    var difficulty = document.getElementById('difficulty').value;
    return difficulty
    }

    let techStack = localStorage.getItem('name');
    console.log(techStack);
    

      function resetTime() { 
      let xmlHttpReq = new XMLHttpRequest();
      TimeReset = 'https://script.google.com/macros/s/AKfycbzz-M5FiX1vQsYBxqeqkhDVjexnHpj0TaNQtS0TTKZJu90_p8HF5TJQXq1FjSc-KNGx/exec?id=Productivity&Task=Resetting&Difficulty=0';
      xmlHttpReq.open("GET", TimeReset, false);       
      xmlHttpReq.send(null);
      return xmlHttpReq.responseText;
    };

    function logNewTask(task, difficulty) {
        var task = getTask();
        var difficulty = getDifficulty();
        let xmlHttpReq = new XMLHttpRequest();
        theUrl = 'https://script.google.com/macros/s/AKfycbzz-M5FiX1vQsYBxqeqkhDVjexnHpj0TaNQtS0TTKZJu90_p8HF5TJQXq1FjSc-KNGx/exec?id=Productivity' + '&Task=' + task + '&Difficulty=' + difficulty;
        xmlHttpReq.open("GET", theUrl, false); 
        xmlHttpReq.send(null);
        return xmlHttpReq.responseText;
      }   

      function endTask(task, difficulty) {
        var task = getTask();
        var difficulty = getDifficulty();
        let xmlHttpReq = new XMLHttpRequest();
        theUrl = 'https://script.google.com/macros/s/AKfycbzz-M5FiX1vQsYBxqeqkhDVjexnHpj0TaNQtS0TTKZJu90_p8HF5TJQXq1FjSc-KNGx/exec?id=Productivity' + '&Task=' + task + '&Difficulty=' + difficulty;
        xmlHttpReq.open("GET", theUrl, false); 
        xmlHttpReq.send(null);
        return xmlHttpReq.responseText;
      }   


  document.getElementById('clickMe').onclick = function()
{
    startStop(); //start the timer
    resetTime(); //initiate poductivity counter
}
  document.getElementById("clickMe").addEventListener('click', logNewTask.bind(null, task, difficulty)); 




document.getElementById("done").addEventListener('click', endTask.bind(null, task, difficulty)); 

