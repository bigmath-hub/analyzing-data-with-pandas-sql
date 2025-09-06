import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pyproj import Geod

def main():
    bh = (-19.9, -43.9)
    toquio = (35.7, 139.7)
    
    
    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_global()
    ax.coastlines()
    ax.add_feature(cfeature.LAND, color="lightgray")
    ax.add_feature(cfeature.OCEAN, color="lightblue")

    # lats, lons = great_circle_points(bh[0], bh[1], toquio[0], toquio[1], n=300)
    print(great_circle_points(bh[0], bh[1], toquio[0], toquio[1], n=300))
    ax.plot(lons, lats, transform=ccrs.Geodetic(), color="red", linewidth=2)

    ax.plot(bh[1], bh[0], "ro", markersize=6, transform=ccrs.Plate.Carree())
    ax.plot(toquio[0], toquio[1], "bo", marquersize=6, transform=ccrs.Plate.Carree())

    ax.set_title("Circulo Max: BH - Toquio")
    plt.show()

def great_circle_points(lat1, lon1, lat2, lon2, n=200):
    geod = Geod(ellps="WGS84")
    lons, lats = geod.npts(lon1, lat1, lon2, lat2, npts=2)
    lons = [lon1] + lons + [lon2]
    lats = [lat1] + lats + [lat2]
    return lats, lons

if __name__ == "__main__":
    main()