document.addEventListener('DOMContentLoaded', async function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('form').onsubmit = async function (event) {
    event.preventDefault();
  
    const recipients = document.querySelector('#compose-recipients').value;
    const body = document.querySelector('#compose-body').value;
    const subject = document.querySelector('#compose-subject').value;
  
    try {
      const response = await fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({ recipients, subject, body }),
      });
  
      const result = await response.json();
  
      if (result.message) {
        alert(result.message);
        document.querySelector('#sent').click();
      } else {
        throw new Error(result.error || 'An error occurred.');
      }
  
    } catch (error) {
      console.error("Error sending email:", error);
      alert(error.message); 
    }
  };
  

});

function compose_email(e, recipients = '', subject = '', body = '') {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

async function archive(id) {
  await fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  load_mailbox('inbox')
}

async function reply(id) {
  await fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(async email => {
      let subject = email.subject;
      if (!subject.startsWith("Re: ")) {
        subject = "Re: " + subject;
      } 
      compose_email(recipients =  email.sender, subject = subject, body = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}`);
    });
}


async function unarchive(id) {
  await fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
  load_mailbox('inbox')
}

async function showEmail(id, mailbox) {
  try {
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    const email = await fetch(`/emails/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Network error: ${response.status}`);
        }
        return response.json(); 
       });

    if (!email.read) {
      await fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ read: true })
      });
    }
    document.querySelector('#emails-view').innerHTML = getHTML(email, mailbox);
  } catch (error) {
    console.error("Error loading email:", error);
  }
}

function getHTML(email, mailbox) {
  const senderOrRecipient = mailbox === 'sent' ? email.recipients.join(', ') : email.sender;
  const toOrFrom = mailbox === 'sent' ? 'To' : 'From';
  const bg = email.read ? 'body-secondary' : 'white';
  const archiveAction = email.archived ? 'unarchive' : 'archive';

  return `
    <div class="d-flex">
      <button type="button" class="btn btn-outline-dark" onclick="load_mailbox('${mailbox}')">
        <i class='fa fa-arrow-left'></i> Back
      </button>
      <button type="button" class="btn btn-outline-warning text-capitalize" style='display: ${mailbox === 'sent' ? 'none' : 'block'}' onclick="${archiveAction}(${email.id})">
        <i class='fa fa-archive'></i> ${archiveAction}
      </button>
    </div>
    <div class="mt-2 card" style='cursor: pointer;'>
      <div class="card-body bg-${bg}">
        <h5 class="card-title">Subject: ${email.subject}</h5>
        <hr>
        <h6 class="card-subtitle mb-2 text-muted">${toOrFrom}: ${senderOrRecipient}</h6>
        <p class="card-subtitle mb-2 text-muted">${email.timestamp}</p>
        <hr>
        <p class="card-subtitle mb-2 text-muted">${email.body}</p>
      </div>
    </div>
    <button type="button" class="float-end btn btn-outline-dark text-capitalize mt-2" onclick="reply(${email.id})">
      <i class='fa fa-reply'></i> Reply
    </button>
  `;
}


async function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  HTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  await fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {


      emails.forEach(email => {
        const senderOrRecipient = mailbox === 'sent' ? email.recipients.join(', ') : email.sender;
        const toOrFrom = mailbox === 'sent' ? 'To' : 'From';
        const bg = email.read === true ? 'body-secondary' : 'white'
        const mark = email.read === true ? 'check' : 'xmark'
        const read = email.read === true ? 'read' : 'unread'
        HTML += `
          <div class="mt-2 card" style="cursor: pointer;" onclick="showEmail(${email.id},\'${mailbox}\')">
            <div class="card-body bg-${bg}">
              <h5 class="card-title">Subject: ${email.subject}</h5>
              <h6 class="card-subtitle mb-2 text-muted">${toOrFrom}: ${senderOrRecipient}</h6>
              <div class="float-end"> 
                <p class="card-subtitle mb-2 text-muted fs-6 fst-italic">${email.timestamp}</p> 
                <p class="text-end card-subtitle mb-2 text-muted fs-6 fst-italic" style='display: ${mailbox === 'sent' ? 'none' : 'block'}'>${read} <i class="fa fa-${mark}"></i></p> 
              </div>
            </div>
          </div>
        `
      });
      document.querySelector('#emails-view').innerHTML = HTML;
    });
}