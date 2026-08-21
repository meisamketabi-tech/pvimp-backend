import React, { useEffect, useState } from "react";
import "./Dashboard.css";


interface OrganizationNode {

    id: number;
    name: string;
    code: string;
    unit_type: string;
    positions: any[];
    children: OrganizationNode[];

}


const typeTitle: any = {

    GENERAL_DIRECTORATE: "اداره کل",
    MANAGEMENT: "حوزه مدیریت",
    DEPUTY: "معاونت",
    DEPARTMENT: "اداره",
    COUNTY_OFFICE: "اداره شهرستان",
    COUNTIES: "ادارات شهرستان",
    UNIT: "واحد"

};



export default function SupervisionOrganizationChart() {


    const [tree, setTree] = useState<OrganizationNode[]>([]);
    const [selected, setSelected] = useState<any>(null);
    const [expanded, setExpanded] = useState<number[]>([]);
    const [loading, setLoading] = useState(false);



    useEffect(() => {


        fetch("http://127.0.0.1:8000/api/v1/organization/tree")

            .then(res => res.json())

            .then(data => {

                setTree(data);

                if (data.length) {

                    setExpanded(
                        data.map((x: any) => x.id)
                    );

                }

            })

            .catch(err => {

                console.error(
                    "Organization tree error:",
                    err
                );

            });


    }, []);





    function toggle(id: number) {

        setExpanded(prev =>

            prev.includes(id)

                ?

                prev.filter(x => x !== id)

                :

                [...prev, id]

        );

    }





    function selectUnit(id: number) {


        setLoading(true);


        fetch(
            `http://127.0.0.1:8000/api/v1/organization/${id}`
        )

            .then(res => res.json())

            .then(data => {

                setSelected(data);

            })

            .finally(() => {

                setLoading(false);

            });


    }





    function renderNode(
        node: OrganizationNode,
        level: number = 0
    ) {


        const open =
            expanded.includes(node.id);


        const hasChildren =
            node.children &&
            node.children.length > 0;



        return (

            <div
                key={node.id}
                style={{
                    marginRight: level * 25
                }}
            >


                <div

                    className="dashboard-card"

                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "10px",
                        cursor: "pointer"
                    }}

                >


                    {

                        hasChildren &&

                        <button

                            onClick={(e) => {

                                e.stopPropagation();

                                toggle(node.id);

                            }}

                        >

                            {
                                open ? "-" : "+"
                            }

                        </button>

                    }



                    <div
                        onClick={() => selectUnit(node.id)}
                    >

                        <b>
                            {node.name}
                        </b>


                        <br />


                        <span>

                            {
                                typeTitle[node.unit_type]
                                ||
                                node.unit_type
                            }

                        </span>



                        <div

                            style={{
                                fontSize: "12px",
                                marginTop: "5px"
                            }}

                        >

                            سمت‌ها:
                            {
                                node.positions?.length || 0
                            }


                            {" | "}


                            زیرمجموعه:
                            {
                                node.children?.length || 0
                            }

                        </div>


                    </div>


                </div>




                {

                    hasChildren &&
                    open &&

                    <div>

                        {

                            node.children.map(

                                child =>

                                    renderNode(
                                        child,
                                        level + 1
                                    )

                            )

                        }

                    </div>

                }



            </div>

        );


    }





    return (

        <div

            className="dashboard-container"

            dir="rtl"

        >



            <div className="expert-header">

                <h1>

                    ساختار سازمانی و مسئولیت‌های نظارتی

                </h1>

            </div>




            <div

                style={{

                    display: "grid",

                    gridTemplateColumns: "2fr 1fr",

                    gap: "20px"

                }}

            >




                <div className="dashboard-card">


                    <h2>

                        درخت سازمان

                    </h2>



                    {

                        tree.map(

                            node =>

                                renderNode(node)

                        )

                    }


                </div>





                <div className="dashboard-card">



                    {

                        loading &&

                        <h3>

                            در حال دریافت اطلاعات...

                        </h3>

                    }




                    {

                        selected && !loading &&

                        <>

                            <h2>

                                {selected.name}

                            </h2>



                            <p>

                                نوع واحد:

                                {" "}

                                {
                                    typeTitle[selected.unit_type]
                                    ||
                                    selected.unit_type
                                }

                            </p>




                            <h3>

                                سمت‌های سازمانی

                            </h3>



                            {

                                selected.positions?.length

                                    ?

                                    selected.positions.map(

                                        (p: any) => (

                                            <div

                                                key={p.id}

                                                style={{

                                                    padding: "8px",

                                                    borderBottom:
                                                        "1px solid #ddd"

                                                }}

                                            >

                                                <b>

                                                    {p.position_title}

                                                </b>


                                                <br />

                                                کد:

                                                {p.position_code}


                                                <br />

                                                افراد منصوب:

                                                {p.assigned_users}


                                            </div>

                                        )

                                    )

                                    :

                                    <p>

                                        سمتی تعریف نشده است

                                    </p>

                            }







                            <h3>

                                مسئولین

                            </h3>



                            {

                                selected.users?.length

                                    ?

                                    selected.users.map(

                                        (u: any) => (

                                            <div

                                                key={u.assignment_id}

                                                style={{

                                                    padding: "8px"

                                                }}

                                            >

                                                <b>

                                                    {u.full_name}

                                                </b>


                                                <br />

                                                سمت:

                                                {u.role}


                                            </div>

                                        )

                                    )

                                    :

                                    <p>

                                        مسئولی ثبت نشده است

                                    </p>

                            }







                            <h3>

                                مسئولیت‌های نظارتی

                            </h3>



                            {

                                selected.responsibilities?.length

                                    ?

                                    selected.responsibilities.map(

                                        (r: any) => (

                                            <div

                                                key={r.id}

                                                style={{

                                                    borderBottom:
                                                        "1px solid #ddd",

                                                    padding: "10px"

                                                }}

                                            >

                                                <b>

                                                    {r.title}

                                                </b>


                                                <br />


                                                شرح:

                                                {r.description}


                                                <br />


                                                نوع بازرسی:

                                                {r.inspection_type}


                                                <br />


                                                اولویت:

                                                {r.priority}


                                            </div>

                                        )

                                    )

                                    :

                                    <p>

                                        مسئولیت نظارتی ثبت نشده است

                                    </p>

                            }


                        </>

                    }





                    {

                        !selected &&
                        !loading &&

                        <p>

                            یک واحد را انتخاب کنید

                        </p>

                    }



                </div>



            </div>



        </div>

    );


}


