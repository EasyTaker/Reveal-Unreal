function getLoginData (username, password, returning, image){
  if (returning == true){
    validateLogin(username, password);
    location = "file:///C:/Users/Baumw/Documents/%23%23Easytaker's%20Studio%23%23/Code/Java%20Script/Hackatron_Site/site/mainPage.html"
  } else {
    createLogin(username, password, returning, image);
  }
}

function validateLogin(username, password){
  return true;
}

function createLogin(username, password, returning, image){
  if Login == uniqueLogin(username, password){
    alert("Your Login is unique. The wild pirate we locked up will create it at some point.");
  } else {
    alert("U think we stupid?");
  }
}
