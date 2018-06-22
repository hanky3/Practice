package com.jaen.o2o.jaenpay;

import android.content.Context;
import android.os.Bundle;
import android.preference.PreferenceFragment;
import android.support.v4.app.Fragment;
import android.support.v4.app.ListFragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

public class SettingFragment extends ListFragment {

	private Context ctx;
	// 이 프레그먼트가 생성되었을때를 구분할 변수
	public static boolean isCreated = false;

	public SettingFragment(Context c) {
		ctx = c;
	}

	// @Override
	// public void onCreate(Bundle savedInstanceState) {
	// // TODO Auto-generated method stub
	// super.onCreate(savedInstanceState);
	// addPreferencesFromResource(R.xml.o2o_config);
	// }

	// @Override
	// public View onCreateView(LayoutInflater inflater, ViewGroup container,
	// Bundle savedInstanceState) {
	// // TODO Auto-generated method stub
	// TextView tv = new TextView(getActivity());
	// tv.setText("Setting");
	// tv.setTextSize(20);
	// tv.setTextColor(getResources().getColor(android.R.color.holo_blue_bright));
	// return tv;
	// }

	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onActivityCreated(savedInstanceState);
		String[] configArr = { "Beacon 서비스 활성화", "NFC 기능 활성화" };
		ArrayAdapter<String> confAdapter = new ArrayAdapter<String>(
				getActivity(), android.R.layout.simple_list_item_checked,
				configArr);

		setListAdapter(confAdapter);
		getListView().setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);

	}

	@Override
	public void onListItemClick(ListView l, View v, int position, long id) {
		// TODO Auto-generated method stub
		super.onListItemClick(l, v, position, id);
		
		Toast.makeText(
				getActivity(),
				l.getAdapter().getItem(position).toString(), Toast.LENGTH_SHORT).show();

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
