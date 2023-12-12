const html = await fetch('../backend/templates/loginview.html')
.then(response => response.text())
.then(data => {
  return data
})

const loginview = {
    template: html
  }
  
export default loginview