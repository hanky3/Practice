package com.jaen.o2o.jaenpay.hce;



import com.jaen.o2o.jaenpay.R;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;

public class HCEMainActivity extends FragmentActivity {
	
	private String accountInfo;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		setContentView(R.layout.hce_main);
		
		Intent i = getIntent();
		accountInfo = i.getStringExtra("account");
		System.out.println("HCEMainActivity ----  accountInfo : "+accountInfo);
		System.out.println("end =================");
		

		if (savedInstanceState == null) {
			FragmentTransaction transaction = getSupportFragmentManager()
					.beginTransaction();
			CardEmulationFragment fragment = new CardEmulationFragment();
			Bundle flagB = new Bundle();
			flagB.putString("card_flag", "new");
			fragment.setArguments(flagB);
			transaction.replace(R.id.card_content_fragment, fragment);
			transaction.commit();
		}

	}

}
