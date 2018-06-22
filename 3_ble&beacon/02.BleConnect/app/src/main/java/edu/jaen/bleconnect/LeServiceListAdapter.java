package edu.jaen.bleconnect;

import java.util.ArrayList;

import android.app.Activity;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGattService;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

public class LeServiceListAdapter extends BaseAdapter {
	private ArrayList<BluetoothGattService> mLeServices;
    private LayoutInflater mInflator;

    public LeServiceListAdapter(Context context) {
        super();
        mLeServices = new ArrayList<BluetoothGattService>();
        mInflator = LayoutInflater.from(context);
    }

    public void addSerivce(BluetoothGattService device) {
        if(!mLeServices.contains(device)) {
        	mLeServices.add(device);
        }
    }
    public void addAll(ArrayList<BluetoothGattService> Services){
    	this.mLeServices = Services;
    }
    public BluetoothGattService getService(int position) {
        return mLeServices.get(position);
    }

    public void clear() {
    	mLeServices.clear();
    }

    @Override
    public int getCount() {
        return mLeServices.size();
    }

    @Override
    public Object getItem(int i) {
        return mLeServices.get(i);
    }

    @Override
    public long getItemId(int i) {
        return i;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        ViewHolder viewHolder;
        // General ListView optimization code.
        if (view == null) {
            view = mInflator.inflate(R.layout.servicelistitem, null);
            viewHolder = new ViewHolder();
            viewHolder.serviceName = (TextView) view.findViewById(R.id.service_name);
            view.setTag(viewHolder);
        } else {
            viewHolder = (ViewHolder) view.getTag();
        }

        BluetoothGattService service = mLeServices.get(i);
        final String serviceUUID = service.getUuid().toString();
        if (serviceUUID.length() > 0){
            viewHolder.serviceName.setText(serviceUUID);
        }
        else
            viewHolder.serviceName.setText("unknown_device");
        return view;
    }
    
    static class ViewHolder {
        TextView serviceName;
    }
    
}
