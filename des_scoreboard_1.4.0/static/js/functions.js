
    // FUNCTION USED TO UPDATE THE COLOUR AND FONT OF THE QUEUED STATUS FIELD
    function updateStatusColour() {
        
        var cells = document.getElementById("queue").getElementsByTagName("a");
        
        // LOOP THROUGH EACH <a> TAG
        for (var i = 0; i < cells.length; i++) {

            // TEST VALUE OF CELL
            if (cells[i].innerHTML == 'PLAYING') {
                // UPDATE FONT
                cells[i].style.color        = '#00afd5';
                cells[i].style.fontWeight   = 'bold';
                cells[i].style.fontSize =   '1.2em';
            }
        }
    }