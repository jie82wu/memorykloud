package com.memorykloud.Activities;

import android.app.ListActivity;
import android.os.Bundle;
import android.widget.*;

public class FriendlistActivity extends ListActivity {

	static final String[] COUNTRIES = new String[] { "Joe Doe", "Alice Wang",
			"Snow White", "Micky Mouse", "Johny Depp" };

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		setListAdapter(new ArrayAdapter<String>(this,
				android.R.layout.simple_list_item_checked, COUNTRIES));

		ListView lv = getListView();
		lv.setTextFilterEnabled(true);
	}
}
