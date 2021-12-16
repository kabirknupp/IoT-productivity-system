chartIt()
async function chartIt(){ //async means it doesnt run in time with everything else
    const data = await getEmailData();
    const data2 = await getSoundData();  
    const data3 = await getProductivityData();            
    //const data = await getData2();
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: data.xs,
        datasets: [{
            label: 'Predicted importance of my E-mails',
            data: data.ys,
            backgroundColor: 
            'rgba(102,204,255,0.7)',
            /*             'rgba(102,204,255,1)',
*/
            borderColor:
            'rgba(102, 255, 255, 1)',
            borderWidth: 1,
            yAxisID: 'y',
        },
        {
            label: 'Sound Fluctuation in my Workspace',
            data: data2.ys,
            backgroundColor: 
            'rgba(253,68,112,0.2)',
            borderColor:
            'rgba(253,68,112,1)',
            borderWidth: 1,
            yAxisID: 'y1',
        },
        {
            label: 'My productivity',
            data: data3.ys,
            backgroundColor: 
                'rgba(102, 153, 255, 0.2)',
            borderColor:
                'rgba(102, 102, 255,1)',
            borderWidth: 1,
            yAxisID: 'y2',
        }
    ]
    },
    options: {
scales: {
    x: {

        display: false,
    },


    y: {
         display: false,
        gridLines: {
            drawBorder: false,
        },    
        grid:{
            display:false
                },

        ticks: {
            display: false
            
        },
        beginAtZero: true
    },
    y1: {
        display: false,
        gridLines: {
            drawBorder: false,
        },    
        grid:{
            display:false
                },
        ticks: {
            // Include a dollar sign in the ticks
            display: false
        }
    },

    y2: {
        display: false,
        grid:{
            display:false
                },
        ticks: {
            // Include a dollar sign in the ticks
            display: false
        }
    },


},
elements: {
line: {
    tension: 0.2 // disables bezier curves
},
point:{
    radius: 2
}
},
}
});
}





async function getEmailData(){ //asynchronous calls with await keyword
const response = await fetch('Email_Data_Clean.csv');
const data = await response.text();
// console.log(data);

const xd = [];
const xs = [];
const ys = [];

const table = data.split(/\n/).slice(1);
//for (let i = 0; i < rows.length; i++)
table.forEach(row => {
const columns = row.split(',')
const unixtimestamp = columns[0];
const dates = new Date(unixtimestamp*1000);
var readableDate = dates.toLocaleDateString("en-UK")
var readableTime = dates.toLocaleTimeString("en-UK")
var [dd, mm, yyyy] = readableDate.split("/"); //make sure to check which way around these are
var dayMonthYear = `${yyyy}-${mm}-${dd}`;
const formattedTime = dayMonthYear.concat(" ", readableTime)
xs.push(unixtimestamp);
xd.push(formattedTime);
const importance = columns[1]
ys.push(parseFloat(importance) + 0); //parseFloat changes this data to a number from a string
console.log(unixtimestamp, importance);
})
return { xd, xs, ys };
//   console.log(rows);
}





async function getSoundData(){ //asynchronous calls with await keyword
const response = await fetch('SoundFlux_Data.csv');
const data = await response.text();
// console.log(data);

const xd = [];
const xs = [];
const ys = [];

const table = data.split(/\n/).slice(1);
//for (let i = 0; i < rows.length; i++)
table.forEach(row => {
const columns = row.split(',')
const unixtimestamp = columns[2];
const dates = new Date(unixtimestamp*1000);
var readableDate = dates.toLocaleDateString("en-UK")
var readableTime = dates.toLocaleTimeString("en-UK")
var [dd, mm, yyyy] = readableDate.split("/"); //make sure to check which way around these are
var dayMonthYear = `${yyyy}-${mm}-${dd}`;
const formattedTime = dayMonthYear.concat(" ", readableTime)
xs.push(unixtimestamp);
xd.push(formattedTime);
const soundFlux = columns[3]
ys.push(parseFloat(soundFlux) + 0); //parseFloat changes this data to a number from a string
console.log(unixtimestamp, soundFlux);
})
return { xd, xs, ys };
//   console.log(rows);
}




async function getProductivityData(){ //asynchronous calls with await keyword
const response = await fetch('Productivity.csv');
const data = await response.text();
// console.log(data);

const xd = [];
const xs = [];
const ys = [];

const table = data.split(/\n/).slice(1);
//for (let i = 0; i < rows.length; i++)
table.forEach(row => {
const columns = row.split(',')
const unixtimestamp = columns[2];
const dates = new Date(unixtimestamp*1000);
var readableDate = dates.toLocaleDateString("en-UK")
var readableTime = dates.toLocaleTimeString("en-UK")
var [dd, mm, yyyy] = readableDate.split("/"); //make sure to check which way around these are
var dayMonthYear = `${yyyy}-${mm}-${dd}`;
const formattedTime = dayMonthYear.concat(" ", readableTime)
xs.push(unixtimestamp);
xd.push(formattedTime);
const productivity = columns[3]
ys.push(parseFloat(productivity) + 0); //parseFloat changes this data to a number from a string
console.log(unixtimestamp, productivity);
})
return { xd, xs, ys };
//   console.log(rows);
}






//plot the other graph underneath for fun
chartSound()

async function chartSound(){ //async means it doesnt run in time with everything else
const data = await getSoundData();
const ctx = document.getElementById('SoundChart').getContext('2d');
const myChart = new Chart(ctx, {
type: 'line',
data: {
labels: data.xd,
datasets: [{
    label: 'Sound Fluctuation in my Workspace',
    data: data.ys,
    backgroundColor: 
        'rgba(255, 99, 132, 0.2)',
    borderColor:
        'rgba(255, 99, 132, 1)',

    borderWidth: 1
}
]
},
options: {
scales: {
x: {
        type: 'time',
        time: {
            unit: 'minute'
        }
    },
y: {
ticks: {
    // Include a dollar sign in the ticks
    callback: function(value, index, values) {
        return  value + ' fluctuations';
    }
}
}
},
elements: {
line: {
tension: 0.04 // disables bezier curves
},
point:{
    radius: 1
}
},
}
});
}


//plot the other graph underneath for fun
chartEmails()

async function chartEmails(){ //async means it doesnt run in time with everything else
const data = await getEmailData();
const ctx = document.getElementById('EmailChart').getContext('2d');
const myChart = new Chart(ctx, {
type: 'line',
data: {
labels: data.xd,
datasets: [{
    label: 'Predicted importance of my E-mails',
    data: data.ys,
    backgroundColor: 
    'rgba(102, 255, 255, 0.2)',
    borderColor:
    'rgba(102,204,255,1)',
    borderWidth: 1
}
]
},
options: {
scales: {
x: {
        type: 'time',
        time: {
            unit: 'minute'
        }
    },
y: {
ticks: {
    // Include a dollar sign in the ticks
    callback: function(value, index, values) {
        return  value + '/10 importance';
    }
}
}
},
elements: {
line: {
tension: 0.04 // disables bezier curves
},
point:{
    radius: 2
}
},
}
});
}



//plot the other graph underneath for fun
chartProductivity()

async function chartProductivity(){ //async means it doesnt run in time with everything else
const data = await getProductivityData();
const ctx = document.getElementById('ProductivityChart').getContext('2d');
const myChart = new Chart(ctx, {
type: 'line',
data: {
labels: data.xd,
datasets: [{
    label: 'Difficulty of my work',
    data: data.ys,
    backgroundColor: 
    'rgba(102, 153, 255, 0.2)',
borderColor:
    'rgba(102, 102, 255,1)',

    borderWidth: 1
}
]
},
options: {
scales: {
x: {
        type: 'time',
        time: {
            unit: 'minute'
        }
    },
y: {
ticks: {
    // Include a dollar sign in the ticks
    callback: function(value, index, values) {
        return  value + '/10 difficulty';
    }
}
}
},
elements: {
line: {
tension: 0.04 // disables bezier curves
},
point:{
    radius: 1
}
},
}
});
}


