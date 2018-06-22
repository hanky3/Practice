package com.jaen.o2o.jaenpay;

import com.jaen.o2o.jaenpay.util.CommonUtilities;



import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class HomeFragment extends Fragment {

	private Context ctx;
	// 이 프레그먼트가 생성되었을때를 구분할 변수
	public static boolean isCreated = false;
	public static final String TAG_NAME = "HomeFragment";

	public HomeFragment(Context c) {
		ctx = c;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		// TextView tv = new TextView(getActivity());
		// tv.setText("Home 라네..");
		// tv.setTextSize(20);
		// tv.setTextColor(getResources().getColor(android.R.color.holo_orange_light));
		View homeView = inflater.inflate(R.layout.home_fraglayout, null);
		Button menuViewBut = (Button) homeView.findViewById(R.id.viewMenuBut);
		menuViewBut.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				viewMenu();
			}
		});
		return homeView;
	}

	@Override
	public void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
	}

	@Override
	public void onResume() {
		// TODO Auto-generated method stub
		super.onResume();
	}

	private void viewMenu() {

		String phoneNum = CommonUtilities.getMyPhoneNum(getActivity());
		Toast.makeText(ctx, "나의 전화 번호 : " + phoneNum, Toast.LENGTH_SHORT)
				.show();
		String url = CommonUtilities.MY_WEB_SERVER
				+ "/O2OProject/main.do?phoneNum=" + phoneNum;
		Log.i(TAG_NAME, url);
		Intent viewMeunI = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
		startActivity(viewMeunI);

	}

}
