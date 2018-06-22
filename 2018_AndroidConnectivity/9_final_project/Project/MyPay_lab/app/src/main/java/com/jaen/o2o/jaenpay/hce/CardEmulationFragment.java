package com.jaen.o2o.jaenpay.hce;

import com.jaen.o2o.jaenpay.R;

import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v4.app.Fragment;
//import android.support.v4.app.Fragment;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;

/**
 * @version 1.0
 * @created 2014-11-25
 * @description 저장된 카드 정보를 프래그먼트에 출력
 * @reference http://developer.android.com/samples/CardEmulation/index.html
 */
public class CardEmulationFragment extends Fragment {

	public static final String TAG = "CardEmulationFragment";

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
	}

	/**
	 * 저장된 카드 정보를 프래그먼트에 출력
	 */
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// Inflate the layout for this fragment
		//Toast.makeText(getActivity(), "CardFrag onCreateView call...", Toast.LENGTH_SHORT).show();
		String viewAccount = AccountStorage.GetAccount(getActivity());
		View v = null;
		if (viewAccount.equals("00000000") || viewAccount == null) {
			v = inflater.inflate(R.layout.card_regi_intro, null);
			return v;
		}
		
		if(getArguments()==null){
			v = inflater.inflate(R.layout.hce_main_test, container, false);
		}else{
			v = inflater.inflate(R.layout.main_fragment, container, false);
		}

		
		EditText account = (EditText) v.findViewById(R.id.card_account_field);
		System.out.println("CardEmulationFragment ----- viewAccount : "
				+ viewAccount);

		LinearLayout ll = new LinearLayout(getActivity());
		ll = (LinearLayout) v.findViewById(R.id.type);

		String accountInfo = "";
		Drawable drawable = null;

		// if(!(viewAccount.equals("00000000")) && viewAccount!=null){

		System.out.println("CardEmulationFragment ----- 55 라인 수행....");

		String snew = viewAccount.replaceAll("\n", ",");
		String snew2 = snew.replace("\t", ",");
		String s = snew2.replaceAll("\\p{Space}", "");
		accountInfo = s.replace("/", ",");
		String[] array = accountInfo.split(",");

		String number = array[0];
		String e_mon = array[1];
		String e_year = array[2];
		String type = array[3].toLowerCase();
		String first_name = array[4];
		String last_name = array[5];

		viewAccount = number.substring(0, 4) + " " + number.substring(4, 8)
				+ " " + number.substring(8, 12) + " "
				+ number.substring(12, 16) + "\n" + e_mon + "/" + e_year + "\n"
				+ first_name + "\t" + last_name;

		if (type.equals("visa")) {
			drawable = getResources().getDrawable(R.drawable.visa);
		} else if (type.equals("mastercard")) {
			drawable = getResources().getDrawable(R.drawable.mastercard);
		} else if (type.equals("maestro")) {
			drawable = getResources().getDrawable(R.drawable.maestro);
		} else if (type.equals("discover")) {
			drawable = getResources().getDrawable(R.drawable.discover);
		} else {
			drawable = getResources().getDrawable(R.drawable.logo_smile_black);
		}

		Button b = new Button(getActivity());
		b.setId(0);
		b.setBackground(drawable);
		LinearLayout.LayoutParams parambtn = new LinearLayout.LayoutParams(
				LinearLayout.LayoutParams.WRAP_CONTENT,
				LinearLayout.LayoutParams.WRAP_CONTENT);
		parambtn.setMargins(10, 55, 0, 0);
		ll.addView(b, parambtn);
		// }
		account.setText(viewAccount);
		// account.addTextChangedListener(new AccountUpdater());
		return v;
	}
	
	@Override
	public void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
		//Toast.makeText(getActivity(), "CardFrag onPause call...", Toast.LENGTH_SHORT).show();
	}
	
	@Override
	public void onResume() {
		// TODO Auto-generated method stub
		super.onResume();
		//Toast.makeText(getActivity(), "CardFrag onResume call...", Toast.LENGTH_SHORT).show();
		
	}

	/**
	 * 카드 재 스캔 등록 시 변동된 카드 정보를 저장
	 */
	private class AccountUpdater implements TextWatcher {
		@Override
		public void beforeTextChanged(CharSequence s, int start, int count,
				int after) {
			// Not implemented.
		}

		@Override
		public void onTextChanged(CharSequence s, int start, int before,
				int count) {
			// Not implemented.
		}

		@Override
		public void afterTextChanged(Editable s) {
			String account = s.toString();
			AccountStorage.SetAccount(getActivity(), account);
		}
	}
}
