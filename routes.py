from flask import request, jsonify, render_template, redirect, url_for, session
from models import UserInformation, House, Building, BuildingAmenity, HomeFeature, Policy
from datetime import datetime
import secrets
import json
from bson import json_util  # 用于处理MongoDB的特殊类型
from pymongo import MongoClient
from bson import ObjectId

def setup_routes(app):
    # 根路由重定向到登录页面
    @app.route('/')
    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/register', strict_slashes=False)
    def register_page():
        try:
            return render_template('register.html')
        except Exception as e:
            print(f"渲染注册页面错误: {str(e)}")
            return str(e), 500

    @app.route('/register/success', methods=['GET'])
    def register_success():
        return render_template('register_success.html')

    @app.route('/register/fail', methods=['GET'])
    def register_fail():
        return render_template('register_fail.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/api/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            
            # 检查用户名和邮箱是否已存在
            if UserInformation.objects(username=data.get('username')).first():
                return jsonify({
                    'success': False,
                    'message': '用户名已存在'
                }), 400
            
            if UserInformation.objects(email=data.get('email')).first():
                return jsonify({
                    'success': False,
                    'message': '邮箱已存在'
                }), 400

            # 创建新用户
            new_user = UserInformation(
                username=data.get('username'),
                password=data.get('password'),
                email=data.get('email'),
                usertype=1 if data.get('isAdmin') else 0,
                avatar="default_avatar.png"  # 设置默认头像
            )
            
            new_user.save()
            
            return jsonify({
                'success': True,
                'message': '注册成功'
            }), 201
            
        except Exception as e:
            print(f"注册错误: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'注册失败: {str(e)}'
            }), 500

    @app.route('/api/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            is_admin = data.get('isAdmin', False)
            
            user = UserInformation.objects(
                username=username,
                password=password
            ).first()
            
            if user:
                if is_admin and user.usertype != 1:
                    return jsonify({
                        'success': False,
                        'message': '非管理员用户，无法进行管理员登录'
                    }), 401
                elif not is_admin and user.usertype == 1:
                    return jsonify({
                        'success': False,
                        'message': '管理员用户，请使用管理员登录'
                    }), 401
                    
                session['user_id'] = str(user.id)
                session['username'] = user.username
                session['usertype'] = user.usertype
                
                return jsonify({
                    'success': True,
                    'message': '登录成功'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': '用户名或密码错误'
                }), 401
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'登录失败: {str(e)}'
            }), 500

    @app.route('/api/users', methods=['GET'])
    def get_users():
        try:
            users = UserInformation.objects.all()
            return jsonify({
                'success': True,
                'users': [
                    {
                        'username': user.username,
                        'email': user.email,
                        'usertype': user.usertype
                    } for user in users
                ]
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500 

    @app.route('/houses')
    def house_list():
        return render_template('house_list.html')

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client['SWE_Project2_Rental_Software']
        
        buildings_data = list(db.buildings.find())
        user = UserInformation.objects.get(id=session['user_id'])
        
        building_list = []
        for building in buildings_data:
            building_data = {
                'id': str(building['_id']),
                'name': building.get('name', 'Unknown'),
                'address': building.get('address', 'N/A'),
                'num_unit': building.get('num_unit', 0),
                'about_info': building.get('about_info', '')
            }
            building_list.append(building_data)
        
        return render_template('dashboard.html', 
                             buildings=building_list,
                             user=user)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login_page'))

    @app.route('/search')
    def search():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        try:
            client = MongoClient('mongodb://localhost:27017/')
            db = client['SWE_Project2_Rental_Software']
            
            # Get search term
            search_term = request.args.get('q', '').strip()
            
            # Only search if there's a search term
            buildings = []
            if search_term:
                # Case-insensitive search for building name
                buildings = list(db.buildings.find({
                    'name': {'$regex': search_term, '$options': 'i'}
                }))
                
                # Process building data
                building_list = []
                for building in buildings:
                    building_data = {
                        'id': str(building['_id']),
                        'name': building.get('name', 'Unknown'),
                        'address': building.get('address', 'N/A'),
                        'num_unit': building.get('num_unit', 0),
                        'about_info': building.get('about_info', '')
                    }
                    building_list.append(building_data)
            else:
                building_list = []
            
            user = UserInformation.objects.get(id=session['user_id'])
            
            return render_template('search.html',
                                 buildings=building_list,
                                 search_term=search_term,
                                 user=user)
                                 
        except Exception as e:
            print(f"Search error: {str(e)}")
            return redirect(url_for('dashboard'))

    @app.route('/api/wishlist/toggle', methods=['POST'])
    def toggle_wishlist():
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        try:
            data = request.get_json()
            building_id = data.get('building_id')
            user_id = session['user_id']
            
            client = MongoClient('mongodb://localhost:27017/')
            db = client['SWE_Project2_Rental_Software']
            
            # 检查是否已经在wishlist中
            existing_wishlist = db.wishlists.find_one({
                'user_id': user_id,
                'building_id': building_id
            })
            
            if existing_wishlist:
                # 如果存在，则删除
                db.wishlists.delete_one({
                    'user_id': user_id,
                    'building_id': building_id
                })
                return jsonify({
                    'success': True,
                    'added': False,
                    'message': 'Removed from wishlist'
                })
            else:
                # 如果不存在，则添加
                db.wishlists.insert_one({
                    'user_id': user_id,
                    'building_id': building_id,
                    'added_date': datetime.now()
                })
                return jsonify({
                    'success': True,
                    'added': True,
                    'message': 'Added to wishlist'
                })
                
        except Exception as e:
            print(f"Wishlist error: {str(e)}")
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500

    @app.route('/building/<building_id>')
    def building_detail(building_id):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        try:
            client = MongoClient('mongodb://localhost:27017/')
            db = client['SWE_Project2_Rental_Software']
            
            # 获取用户信息，检查是否是管理员
            user = UserInformation.objects.get(id=session['user_id'])
            is_admin = user.usertype == 1  # 检查用户类型
            
            # 获取建筑信息
            building = db.buildings.find_one({'_id': ObjectId(building_id)})
            if not building:
                return redirect(url_for('dashboard'))
            
            # 获取关联数据
            building_amenities = db.building_amenities.find_one({'_id': building.get('amenities_id')})
            home_features = db.home_features.find_one({'_id': building.get('home_feature_id')})
            policies = db.policies.find_one({'_id': building.get('policy_id')})
            
            # 处理建筑数据
            building_data = {
                'id': str(building['_id']),
                'name': building.get('name', 'Unknown'),
                'address': building.get('address', 'N/A'),
                'num_unit': building.get('num_unit', 0),
                'about_info': building.get('about_info', '')
            }
            
            # 根据用户类型选择不同的模板
            template = 'admin_building_detail.html' if is_admin else 'building_detail.html'
            
            return render_template(template,
                                 building=building_data,
                                 amenities=building_amenities,
                                 features=home_features,
                                 policies=policies,
                                 user=user)
                             
        except Exception as e:
            print(f"Building detail error: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return redirect(url_for('dashboard'))

    @app.route('/admin/building/<building_id>')
    def admin_building_detail(building_id):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        # 检查是否是管理员
        user = UserInformation.objects.get(id=session['user_id'])
        if user.usertype != 1:  # 假设1是管理员类型
            return redirect(url_for('building_detail', building_id=building_id))
        
        try:
            client = MongoClient('mongodb://localhost:27017/')
            db = client['SWE_Project2_Rental_Software']
            
            # 获取建筑信息
            building = db.buildings.find_one({'_id': ObjectId(building_id)})
            if not building:
                return redirect(url_for('dashboard'))
            
            # 获取关联数据
            building_amenities = db.building_amenities.find_one({'_id': building.get('amenities_id')})
            home_features = db.home_features.find_one({'_id': building.get('home_feature_id')})
            policies = db.policies.find_one({'_id': building.get('policy_id')})
            
            return render_template('admin_building_detail.html',
                                 building=building,
                                 amenities=building_amenities,
                                 features=home_features,
                                 policies=policies,
                                 user=user)
                             
        except Exception as e:
            print(f"Admin building detail error: {str(e)}")
            return redirect(url_for('dashboard'))

    @app.route('/api/admin/building/<building_id>/update', methods=['POST'])
    def update_building(building_id):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        # 检查是否是管理员
        user = UserInformation.objects.get(id=session['user_id'])
        if user.usertype != 1:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        
        try:
            data = request.get_json()
            client = MongoClient('mongodb://localhost:27017/')
            db = client['SWE_Project2_Rental_Software']
            
            # 获取当前建筑信息
            building = db.buildings.find_one({'_id': ObjectId(building_id)})
            if not building:
                return jsonify({'success': False, 'message': 'Building not found'}), 404

            # 更新建筑基本信息
            db.buildings.update_one(
                {'_id': ObjectId(building_id)},
                {'$set': data['building']}
            )
            
            # 如果没有关联ID，先创建新的记录
            if 'amenities_id' not in building:
                amenities_result = db.building_amenities.insert_one(data['amenities'])
                amenities_id = amenities_result.inserted_id
                db.buildings.update_one(
                    {'_id': ObjectId(building_id)},
                    {'$set': {'amenities_id': amenities_id}}
                )
            else:
                # 更新现有的建筑设施
                db.building_amenities.update_one(
                    {'_id': building['amenities_id']},
                    {'$set': data['amenities']}
                )
            
            if 'home_feature_id' not in building:
                features_result = db.home_features.insert_one(data['features'])
                features_id = features_result.inserted_id
                db.buildings.update_one(
                    {'_id': ObjectId(building_id)},
                    {'$set': {'home_feature_id': features_id}}
                )
            else:
                # 更新现有的房屋特色
                db.home_features.update_one(
                    {'_id': building['home_feature_id']},
                    {'$set': data['features']}
                )
            
            if 'policy_id' not in building:
                policies_result = db.policies.insert_one(data['policies'])
                policy_id = policies_result.inserted_id
                db.buildings.update_one(
                    {'_id': ObjectId(building_id)},
                    {'$set': {'policy_id': policy_id}}
                )
            else:
                # 更新现有的租赁政策
                db.policies.update_one(
                    {'_id': building['policy_id']},
                    {'$set': data['policies']}
                )
            
            return jsonify({
                'success': True,
                'message': 'Building information updated successfully'
            })
            
        except Exception as e:
            print(f"Update building error: {str(e)}")
            import traceback
            print(traceback.format_exc())  # 打印详细错误信息
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500