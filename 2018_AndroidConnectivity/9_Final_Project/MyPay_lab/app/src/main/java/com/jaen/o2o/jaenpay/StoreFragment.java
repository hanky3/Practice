package com.jaen.o2o.jaenpay;


//import android.app.ListFragment;
import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.ListFragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

public class StoreFragment extends ListFragment {

	private Context ctx;
	// 이 프레그먼트가 생성되었을때를 구분할 변수
	public static boolean isCreated = false;

	public StoreFragment(Context c) {
		ctx = c;
	}

	// @Override
	// public View onCreateView(LayoutInflater inflater, ViewGroup container,
	// Bundle savedInstanceState) {
	// // TODO Auto-generated method stub
	// TextView tv = new TextView(getActivity());
	// tv.setText("가게 정보");
	// tv.setTextSize(20);
	// tv.setTextColor(getResources().getColor(android.R.color.holo_green_light));
	// return tv;
	// }

	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onActivityCreated(savedInstanceState);
		String[] storeArr = { "스토박스 커피점", "남자둘이 하는 떡뽂이집", "돌돌치킨", "길동이네 분식",
				"핫한 짬뽕집", "버거퀸", "NFC 서초점", "탐 앤 제리 커피" };
		ArrayAdapter<String> storeA = new ArrayAdapter<String>(getActivity(),
				android.R.layout.simple_list_item_1, storeArr);
		setListAdapter(storeA);
	}

	@Override
	public void onListItemClick(ListView l, View v, int position, long id) {
		// TODO Auto-generated method stub
		super.onListItemClick(l, v, position, id);
		Toast.makeText(getActivity(),
				"어서오세요 " + (l.getAdapter().getItem(position).toString()),
				Toast.LENGTH_SHORT).show();
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
