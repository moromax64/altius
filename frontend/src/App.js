import { useState } from "react";
import LoginForm from "./components/LoginForm";
import './App.css';
 import 'bootstrap/dist/css/bootstrap.min.css';

function dealCards(deals){
  return (
    <div className="row g-2 justify-content-evenly">
      {deals.map((deal, i) => (
        <div key={i} className="col col-3 custom-card">
          <h3 className="title">{deal.title}</h3>
          {deal.created_at && <p className="cardInfo">{new Date(deal.created_at).toLocaleString()}</p>}
          <p className="cardInfo">Status: {deal.deal_status}</p>
          <p className="cardInfo">Currency: {deal.currency}</p>
          <p className="description">{deal.text}</p>
          {deal.fileUrl && <a href={deal.fileUrl} download className="attachmentLink">View attachment</a>}
        </div>
      ))}
    </div>
  )
}

export default function App() {
  const [response, setResponse] = useState(null);

  return (
    <div className="mainContainer">
        {!response?.ok && <h2 className="mainTitle">Site Crawler</h2>}
        {response && !response?.ok && <h4 className="errorMsg">{response.errorMessage}</h4>}
        {!response?.ok && <LoginForm onResult={setResponse} />}
        {response?.ok && (
          <div className="welcomeElm">
            {response?.user?.account?.logo_url && <img src={response.user.account.logo_url} alt="User logo" className="logo"></img>}
            <h4 className="d-inline ms-4">Welcome back {response.user.full_name}!</h4>
          </div>
        )}
        {response?.ok && response.deals?.length &&
          <div>
            <h3 className="my-5">Your deals:</h3>
            <div className="container-fluid">
                {dealCards(response.deals)}
            </div>
          </div>}
    </div>
  );
}