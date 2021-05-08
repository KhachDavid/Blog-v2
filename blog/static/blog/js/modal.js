/**
 * @author David Khachatryan
 * @copyright Copyright 2021, Mat Ognutyun
 * @license GPL
 * @version 2.0.0
 * @host David Khachatryan
 * @email dkhachatryan@wisc.edu
 * @status production
 */

 var modal = document.getElementById("myModal");

 // Get the buttons that opens the modal
 var btn = document.querySelectorAll("#like-dislike-button-");
   
 // Get the <span> element that closes the modal
 var span = document.getElementsByClassName("close")[0];
   
 // When the user clicks on <span> (x), close the modal
 try {
     span.onclick = function() {
         modal.style.display = "none";
     }
 } 
 
 catch (error) {
 
 }
   
 // When the user clicks anywhere outside of the modal, close it
 window.onclick = function(event) {
     if (event.target == modal) {
         modal.style.display = "none";
     }
 }
  
 // When the user clicks the button, open the modal 
 btn.forEach(b => {
     b.onclick = function() {
         modal.style.display = "block";
     }
 });