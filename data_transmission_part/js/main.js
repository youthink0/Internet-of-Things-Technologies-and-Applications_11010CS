var date = "";
// Given a date in above format, return
// previous day as a date object
function getYesterday(d) 
{
    d = stringToDate(d);
    d.setDate(d.getDate() - 1)
    return d;
}

function print_date_message()
{
    // `date` is a `Date` object
    const formatYmd = date => date.toISOString().slice(0, 10);
    var now = new Date();
    var day_diff = 1000 * 60 * 60 * 24 * 1;
    var flag = 1; //if user want to show invalid records table, then flag = 0, otherwise flag = 1
    var e = document.getElementById("dates").value;
    date = String(formatYmd(now)); 
    //window.alert(date_var);

    if (e=="today")
    {
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(now)); 
        date = String(formatYmd(now));  
        //date = "2022-01-02";   
    }
    else if (e=="yesterday")
    {
        var d = new Date(now - day_diff*1);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        //date = String(formatYmd(d));
        date = "2022-01-02";    
    }     
    else if (e=="2days")
    {
        var d = new Date(now - day_diff*2);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        //date = String(formatYmd(d));  
        date = "2022-01-01";   
    } 
    else if (e=="3days")
    {
        var d = new Date(now - day_diff*3);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        //date = String(formatYmd(d));
        date = "2021-12-31";
    } 
    else if (e=="4days")
    {
        var d = new Date(now - day_diff*4);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        //date = String(formatYmd(d));
        date = "2021-12-30";
    }
    else if (e=="5days")
    {
        var d = new Date(now - day_diff*5);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        //date = String(formatYmd(d));
        date = "2021-12-29";
    }
    else if (e=="6days")
    {
        var d = new Date(now - day_diff*6);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        //date = String(formatYmd(d));
        date = "2021-12-28";
    }
    else if (e=="invalid")
    {
        document.getElementById('table').src = "picture/" + "Invalid Records" + ".png";
        document.getElementById('imageBox').src = ""; 
        document.getElementById('imageBox1').src = "";
        document.getElementById('imageBox2').src = "";
        document.getElementById('imageBox3').src = "";
        flag = 0;
    }
    
    if (flag == 1)
    {
        document.getElementById('table').src = "";
        document.getElementById('imageBox').src = "picture/" + date + "_Line chart" + ".png"; 
        document.getElementById('imageBox1').src = "picture/" + date + " supply_use ratio" + ".png";
        document.getElementById('imageBox2').src = "picture/" + date + " time_use ratio" + ".png";
        document.getElementById('imageBox3').src = "picture/" + date + "_table" + ".png";       
    }
}

function initialize()
{
    document.getElementById( 
                    "message").innerHTML = "顯示日期 : 無";
    date = "";
    flag = 1;
    document.getElementById('table').src = "";
    document.getElementById('imageBox').src = "";
    document.getElementById('imageBox1').src = "";
    document.getElementById('imageBox2').src = "";
    document.getElementById('imageBox3').src = "";
}

window.onload = function()
{ 
    print_date_message();
    initialize();
  
};
