package edu.jaen.android.nfc.appLauncher;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import android.os.Bundle;
import android.app.Activity;
import android.app.ListActivity;
import android.content.ComponentName;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class MainActivity extends Activity {

	ArrayList<AppInfo> launchList = new ArrayList<AppInfo>();
	LayoutInflater inflator;

	@Override
	public void onCreate(Bundle savedInstanceState) {

		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		inflator = (LayoutInflater) getSystemService("layout_inflater");

		findViewById(R.id.showAppListBut).setOnClickListener(
				new View.OnClickListener() {

					public void onClick(View v) {
						// TODO Auto-generated method stub
						showAppList();

					}
				});

	}

	public void showAppList() {

		ViewGroup vGroup = (ViewGroup) inflator.inflate(R.layout.applistlayout,
				null);
		ListView appListView = (ListView) vGroup.findViewById(R.id.appListview);
		
		appListView.setChoiceMode(ListView.CHOICE_MODE_SINGLE);

		PackageManager pkgManager = getPackageManager();

		// 조회할 Action명의 IntentFilter 값 설정
		Intent intent = new Intent(Intent.ACTION_MAIN, null);
		intent.addCategory(Intent.CATEGORY_LAUNCHER);

		List<ResolveInfo> resInfo = pkgManager.queryIntentActivities(intent, 0);
		Collections.sort(resInfo, new ResolveInfo.DisplayNameComparator(
				pkgManager));
		System.out.println("53 : Launch 프로그램 수 ===" + resInfo.size());

		System.out.println("=========================================");

		for (int i = 0; i < resInfo.size(); i++) {

			ResolveInfo launchInfo = resInfo.get(i);

			String packageName = launchInfo.activityInfo.applicationInfo.packageName;
			String appTitle = (String) launchInfo.loadLabel(pkgManager);
			// System.out
			// .println(launchInfo.activityInfo.applicationInfo.packageName
			// + " : name = " + launchInfo.activityInfo.name);
			// System.out.println("title ===" +
			// launchInfo.loadLabel(pkgManager));
			launchList.add(new AppInfo(appTitle, packageName));
		}

		ArrayAdapter<AppInfo> appAdapter = new ArrayAdapter<AppInfo>(this,
				android.R.layout.simple_list_item_single_choice, launchList);

		appListView.setAdapter(appAdapter);

		addEvent(appListView);

		setContentView(vGroup);

	}

	public void addEvent(final ListView listV) {

		listV.setOnItemClickListener(new AdapterView.OnItemClickListener() {

			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {

				ArrayAdapter<AppInfo> adpater = (ArrayAdapter<AppInfo>) listV
						.getAdapter();
				AppInfo info = adpater.getItem(position);
				Toast.makeText(MainActivity.this,
						info.getAppTitle() + ", " + info.getAppPackage(), 1)
						.show();

			}

		});

	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.activity_main, menu);
		return true;
	}
}
