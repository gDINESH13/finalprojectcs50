document.addEventListener('DOMContentLoaded',trail);

function trail()
{
	try
		{
		wishlist_button=document.querySelector('#wishlist');
		wishlist();
		}
	catch(err)
		{
			console.log(err);
		}

	try
	{
		rent_button=document.querySelector('#rent');
		rent();
	}
	catch(err)
	{
		console.log(err);
	}
	try
	{
		document.querySelectorAll('#Accept').forEach(but=>{

			but.addEventListener('click',event=>accept(but));
			//but.onclick=()=>{ alert(`${but.className}`) }
		});
		document.querySelectorAll("#Decline").forEach(but=>
		{
			but.addEventListener('click',event=>decline(but));
		});
	}
	catch(err)
	{
		console.log(err);
	}
	try
	{
		document.querySelectorAll('#endrent').forEach(but=>
		{
			but.addEventListener('click',event=>endrent(but));
		});
	}
	catch(err)
	{
		console.log(err);
	}
}

function wishlist()
{
		wishlist_button.addEventListener('click',()=>{
		
		btn_text=wishlist_button.innerHTML;
		wishlist_pk=wishlist_button.getAttribute('data-id');

		let exists=true
		if (btn_text=="Add to wishlist")
		{
			//alert('yes');
			 exists=false
			 wishlist_button.innerHTML="Remove from wishlist";
			 wishlist_button.className="btn btn-outline-danger btn-sm";
		}
		
		if (exists == true)
		{
			wishlist_button.innerHTML="Add to wishlist";
			wishlist_button.className="btn btn-outline-success btn-sm";
		}
		//alert(`${m}`);

		fetch(`/add_remove_wishlist`,{
		method:'POST',
		body:JSON.stringify({
				list_pk:wishlist_pk,
				exists:exists
			})
			})
		.then(response=>response.json())
		.then(result=>
			{
				console.log(result.message);

			})	

		});	
}

function rent()

{
		rent_button=document.querySelector('#rent');
		rent_button.addEventListener('click',()=>{
		
			btn_text=rent_button.innerHTML;
			car_id=rent_button.getAttribute('data-id');
			

			let exists=true;
			if (btn_text=="Ask for rent")
			{
			 exists=false;
			 rent_button.innerHTML="Changed my mind";
			 rent_button.className="btn btn-outline-danger btn-sm";
			}
		
			if (exists == true)
			{
			 rent_button.innerHTML="Ask for rent";
			 rent_button.className="btn btn-outline-success btn-sm";
			}


			fetch(`/ask_for_rent`,{
			method:'POST',
			body:JSON.stringify({
				car_pk:car_id,
				exists:exists
				})
				})
			.then(response=>response.json())
			.then(result=>
			{
				console.log(result.message);

			})
		});
	
}
function accept(but)
{
	// if owner accpets one users request the other requests are discarded
	name=but.getAttribute('data-name');
	car=but.getAttribute('data-car');
	//alert(`${name}`);
	v=document.querySelector(`#usersList${car}`);
	v.style.display='None';
	x=document.querySelector(`#confirmRent${car}`);
	x.style.display="block";
	
	// a link to the user profile whose request for rent is accepted.
	var a = document.createElement('a');   
    a.innerHTML= `${name}`; 
    a.title = `${name}`;  
    a.href = "/list/1"; 
    x.appendChild(a); 

    fetch(`/accept`,{
			method:'POST',
			body:JSON.stringify({
				carid:car,
				name:name
				})
				})
			.then(response=>response.json())
			.then(result=>
			{
				console.log(result.message);

			});

}

function decline(but)
{
	name=but.getAttribute('data-name');
	car=but.getAttribute('data-car');
	v=document.querySelector(`#SingleUser${name}${car}`);
	//console.log(`#SingleUser${name}${car}`);
	//console.log(`${v.id}`);
	v.style.display='None';
			fetch(`/decline`,{
			method:'POST',
			body:JSON.stringify({
				carid:car,
				name:name
				})
				})
			.then(response=>response.json())
			.then(result=>
			{
				console.log(result.message);

			});
		
}

function endrent(but)
{
	car_id=but.getAttribute('data-id');
	user=but.getAttribute('data-name');
	//confirm(`${car_id}`);
	if(confirm(`Are you sure to end the rent of your  car to ${user}?`)===true)
		{
			//console.log("insideif");
			fetch(`/endrent`,{
			method:'POST',
			body:JSON.stringify({
				carid:car_id,
				name:user
				})
				})
			.then(response=>response.json())
			.then(result=>
			{
				console.log(result.message);
				
				
			});
			document.querySelector(`#div1${car_id}`).style.display='None';
				document.querySelector(`#div2${car_id}`).style.display='None';
				document.querySelector(`#div3${car_id}`).style.display='block';
		}
	
}