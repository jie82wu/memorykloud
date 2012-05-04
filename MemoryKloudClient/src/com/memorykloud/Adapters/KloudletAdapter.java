package com.memorykloud.Adapters;

import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.BaseAdapter;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.memorykloud.R;
import com.memorykloud.Activities.MomentManagerActivity;
import com.memorykloud.Activities.MomentViewerActivity;
import com.memorykloud.Adapters.MomentAdapter.ViewHolder;

public class KloudletAdapter extends BaseAdapter implements Filterable {
	private LayoutInflater _inflater;
	private Context _context;
	private JSONArray _jArray;
	private List<ViewHolder> _holderList;

	public KloudletAdapter(Context context) {
		// Cache the LayoutInflate to avoid asking for a new one each time.
		_inflater = LayoutInflater.from(context);
		this._context = context;
		_holderList = new ArrayList<ViewHolder>();
	}

	public void SetJSONArray(JSONArray jArray) {
		this._jArray = jArray;
	}

	/**
	 * Make a view to hold each row.
	 * 
	 * @see android.widget.ListAdapter#getView(int, android.view.View,
	 *      android.view.ViewGroup)
	 */
	@Override
	public View getView(final int position, View convertView, ViewGroup parent) {
		// A ViewHolder keeps references to children views to avoid
		// unneccessary calls
		// to findViewById() on each row.
		ViewHolder holder;

		// When convertView is not null, we can reuse it directly, there is
		// no need to reinflate it. We only inflate a new View when the
		// convertView
		// supplied by ListView is null.
		// if (convertView == null) {
		convertView = _inflater.inflate(R.layout.mk_kloudlet, null);

		// Creates a ViewHolder and store references to the two children
		// views we want to bind data to.
		holder = new ViewHolder();
		holder.setKloudlet_coverImage((ImageView) convertView
				.findViewById(R.id.picture));
		holder.setKloudlet_Name((TextView) convertView
				.findViewById(R.id.kloudletTitle));

		// Bind the data efficiently with the holder.
		try {
			JSONObject json_data = _jArray.getJSONObject(position);
			holder.getKloudlet_Name().setText(json_data.getString("NAME"));
			holder.setKloudlet_Id(json_data.getInt("ID"));

			String blob_str = json_data.getString("BLOBDATA");
			if (!blob_str.equals("None")) {
				int flags = Base64.DEFAULT;
				byte[] bin = Base64.decode(blob_str, flags);
				Bitmap bm = BitmapFactory.decodeByteArray(bin, 0, bin.length);
				holder.kloudlet_coverImage.setImageBitmap(bm);
			} else {
				// TODO: should completely destroy the imageview
				// holder.imageView.setImageDrawable(null);
			}

		} catch (JSONException e) {
			Log.e("log_tag", "Error processing JSON " + e.toString());
		}

		convertView.setTag(holder);

		_holderList.add(holder);
		return convertView;
	}

	public static class ViewHolder {
		private TextView kloudlet_Name;
		private ImageView kloudlet_coverImage;
		private int kloudlet_Id;

		public int getKloudlet_Id() {
			return kloudlet_Id;
		}

		void setKloudlet_Id(int kloudlet_Id) {
			this.kloudlet_Id = kloudlet_Id;
		}

		public TextView getKloudlet_Name() {
			return kloudlet_Name;
		}

		void setKloudlet_Name(TextView kloudlet_Name) {
			this.kloudlet_Name = kloudlet_Name;
		}

		public ImageView getKloudlet_coverImage() {
			return kloudlet_coverImage;
		}

		void setKloudlet_coverImage(ImageView kloudlet_coverImage) {
			this.kloudlet_coverImage = kloudlet_coverImage;
		}
	}

	@Override
	public Filter getFilter() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public long getItemId(int position) {
		// TODO Auto-generated method stub
		return position;
	}

	@Override
	public int getCount() {
		// TODO Auto-generated method stub
		return _jArray.length();
	}

	@Override
	public Object getItem(int position) {
		// TODO Auto-generated method stub
		return _holderList.get(position);
	}
}
