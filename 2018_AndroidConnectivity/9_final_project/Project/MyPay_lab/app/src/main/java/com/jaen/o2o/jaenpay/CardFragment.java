package com.jaen.o2o.jaenpay;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class CardFragment extends Fragment {

	private Context ctx;
	// 이 프레그먼트가 생성되었을때를 구분할 변수
	public static boolean isCreated = false;
	
	
	public CardFragment(Context c) {
		ctx = c;
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		TextView tv = new TextView(getActivity());
		tv.setText("카드 정보");
		tv.setTextSize(20);
		tv.setTextColor(getResources().getColor(android.R.color.holo_red_light));
		return tv;
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
	
	

}
